FROM nginx:1.23.1-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY privkey.pem /etc/nginx/ssl/live/example.org/privkey.pem
COPY fullchain.pem /etc/nginx/ssl/live/example.org/fullchain.pem