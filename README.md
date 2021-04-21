# face-recognition
Face recognition services

Face recognition services is a docker micro service used to train and score facenet-pytorch algorithms to recognize faces on pictures.

Usage : 
- docker-compose -d up

It will instantiate :
- a mongodb to store face encodings
- a python container to run the python facenet models
- an nginx container to host small training / test scoring UI

Then you can train your model with the UI, uploading photo and tagging every faces recognized, or by invoking python container services :
- http://<host>:<8080>/faceslocation with POST method. The body must include a form data with value "file", and the picture attached. This will return the coordinates of all faces detected in the picture
- http://<host>:<8080>/faces?id=<person> with POST method. The body must include a form data with value "file", and the picture attached. This will train the model to recognize the person identified on the picture. Be careful : only one face per image is allowed
- http://<host>:<8080>/ with POST method. The body must include a form data with value "file", and the picture attached. This will score the image and return locations and name recognized on the picture.
