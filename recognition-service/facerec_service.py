from os import listdir, remove
from os.path import isfile, join, splitext
import sys
from pymongo import MongoClient
import os
import urllib.parse

import face_recognition
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest


db = None

# Global storage for images
#faces_dict = {}
#persistent_faces = ""
#args[0]

# Create flask app
app = Flask(__name__)
CORS(app)

# <Picture functions> #


def is_picture(filename):
    image_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in image_extensions


# def get_all_picture_files(path):
#     files_in_dir = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
#     return [f for f in files_in_dir if is_picture(f)]


def remove_file_ext(filename):
    return splitext(filename.rsplit('/', 1)[-1])[0]

def calc_face_encoding(image):
    # Currently only use first face found on picture
    loaded_image = face_recognition.load_image_file(image)
    faces = face_recognition.face_encodings(loaded_image)

    # If more than one face on the given image was found -> error
    if len(faces) > 1:
        raise Exception(
            "Found more than one face in the given training image.")

    # If none face on the given image was found -> error
    if not faces:
        raise Exception("Could not find any face in the given training image.")

    return faces[0]


# def get_faces_dict(path):
#     image_files = get_all_picture_files(path)
#     return dict([(remove_file_ext(image), calc_face_encoding(image))
#         for image in image_files])


def detect_faces_locations_in_image(file_stream):
    img = face_recognition.load_image_file(file_stream)

    # Get face encodings for any faces in the uploaded image
    face_locations = face_recognition.face_locations(img)
    return face_locations

def detect_faces_in_image(file_stream):
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)

    # Get face encodings for any faces in the uploaded image
    uploaded_faces = face_recognition.face_encodings(img)
    face_locations = face_recognition.face_locations(img)
    

    # Defaults for the result object
    faces_found = len(uploaded_faces)
    faces = []


    if faces_found:
        persons = get_persons()
        for person in persons:
            face_encodings = list(person['encodings'])

            for uploaded_face in uploaded_faces:
                match_results = face_recognition.compare_faces(face_encodings, uploaded_face)
                for idx, match in enumerate(match_results):
                    if match:
                        match = person['name']
                        match_encoding = face_encodings[idx]
                        dist = face_recognition.face_distance([match_encoding],
                                uploaded_face)[0]
                        faces.append({
                            "id": match,
                            "dist": dist,
                            "location": face_locations[idx]
                        })

    return {
        "count": len(faces),
        "faces": faces
    }

# <Picture functions> #

# <DAO> #
def get_person(id):
    return db.persons.find_one({'name': id})

def get_persons():
    return db.persons.find()

def get_persons_names():
    return list(map(lambda person: person['name'] ,get_persons()))

def addEncodings(id, encodings = None):
    if id in get_persons_names():
        person = get_person(id)
        if  encodings is not None:
            person['encodings'].append(encodings.tolist())
            db.persons.find_one_and_update( 
                { "_id" : ObjectId(person._id)},
                {
                    '$set': {
                        'encodings': person['encodings']
                    }
                })
        return get_person(id)
    else:
        person = { 'name': id, 'encodings': []}
        if encodings is not None:
            person['encodings'].append(encodings.tolist())

        db.persons.insert_one(person)
        return get_person(id)

def clearEncodings(id):
    removePerson(id)
    addEncodings(id)

def removePerson(id):
    db.persons.remove({'name':id})

# <Controller>


@app.route('/', methods=['POST'])
def web_recognize():
    file = extract_image(request)

    if file and is_picture(file.filename):
        # The image file seems valid! Detect faces and return the result.
        return jsonify(detect_faces_in_image(file))
    else:
        raise BadRequest("Given file is invalid!")


@app.route('/faceslocation', methods=['POST'])
def web_facelocation():
    file = extract_image(request)
    return jsonify(detect_faces_locations_in_image(file))

@app.route('/faces', methods=['GET'])
def web_get_faces():
    return jsonify(get_persons_names())

@app.route('/faces', methods=['POST'])
def web_faces():
    # POST/DELETE
    file = extract_image(request)
    if 'id' not in request.args:
        raise BadRequest("Identifier for the face was not given!")

    if request.method == 'POST':
        app.logger.info('%s loaded', file.filename)
        # HINT jpg included just for the image check -> this is faster then passing boolean var through few methods
        # TODO add method for extension persistence - do not forget abut the deletion
        #file.save("{0}/{1}.jpg".format(persistent_faces, request.args.get('id')))
        try:
            new_encoding = calc_face_encoding(file)
            addEncodings(request.args.get('id'), new_encoding)
        except Exception as exception:
            raise BadRequest(exception)

    return "done"


@app.route('/faces', methods=['DELETE'])
def web_delete_faces():
    if 'id' not in request.args:
        raise BadRequest("Identifier for the face was not given!")

    removePerson(request.args.get('id'))

    return "done"

def extract_image(request):
    # Check if a valid image file was uploaded
    if 'file' not in request.files:
        raise BadRequest("Missing file parameter!")

    file = request.files['file']
    if file.filename == '':
        raise BadRequest("Given file is invalid")

    return file
# </Controller>


if __name__ == "__main__":    

    print("Connecting to database...")
    dbhostname = urllib.parse.quote_plus(os.getenv('DATABASE_HOSTNAME'))
    dbport = int(urllib.parse.quote_plus(os.getenv('DATABASE_PORT')))
    dbname = urllib.parse.quote_plus(os.getenv('MONGO_INITDB_DATABASE'))
    dbuser = urllib.parse.quote_plus(os.getenv('MONGO_INITDB_ROOT_USERNAME'))
    dbpassword = urllib.parse.quote_plus(os.getenv('MONGO_INITDB_ROOT_PASSWORD'))

    URI="mongodb://%s:%s@%s:%d" % (dbuser, dbpassword, dbhostname,dbport)
    client = MongoClient(URI);

    db = client[dbname]

    # Start app
    print("Starting WebServer...")
    app.run(host='0.0.0.0', port=8080, debug=False)
