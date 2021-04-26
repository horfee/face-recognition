FROM nginx:latest

#ADD web/build-modern/* /usr/share/nginx/html
ADD web/face-image.bundled.js /usr/share/nginx/html
ADD web/images /usr/share/nginx/html/images
ADD web/index.html /usr/share/nginx/html
ADD web/styles.css /usr/share/nginx/html
ADD web/node_modules/file-drop-element/dist/filedrop.umd.js /usr/share/nginx/html

EXPOSE 80 443
