FROM nginx:latest

RUN rm -v /etc/nginx/nginx.conf
COPY ./nginx/nginx.conf /etc/nginx/

RUN mkdir /nginx
COPY /server/staticfiles /nginx/staticfiles
