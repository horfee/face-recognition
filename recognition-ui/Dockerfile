FROM nginx:latest

#ADD web/build-modern/* /usr/share/nginx/html
ADD web/Face-Image.js /usr/share/nginx/html
ADD web/images /usr/share/nginx/html/images
ADD web/index.html /usr/share/nginx/html
ADD web/node_modules/file-drop-element/dist/filedrop.mjs /usr/share/nginx/html/node_modules/file-drop-element/dist/filedrop.mjs

EXPOSE 80 443
