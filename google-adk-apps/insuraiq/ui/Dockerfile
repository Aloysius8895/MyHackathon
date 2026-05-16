#After building using ng build use this dockerfile to deploy

FROM nginx:stable-alpine

RUN rm /usr/share/nginx/html/index.html

COPY ./www/browser /usr/share/nginx/html

EXPOSE 80