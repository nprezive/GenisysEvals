FROM nginx:mainline-alpine

RUN apk add -q --no-cache python3 openssl
RUN pip3 install -q -U pip setuptools Jinja2==2.8

RUN rm /etc/nginx/nginx.conf
RUN rm /etc/nginx/mime.types
COPY conf.d/nginx.conf /etc/nginx/nginx.conf
COPY conf.d/mime.types /etc/nginx/mime.types

RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir /dockersible
COPY dockersible/ /dockersible
COPY backend.conf.j2 /
COPY install.py /

RUN mkdir /certificates
VOLUME ["/certificates"]

COPY entrypoint.sh /
RUN chmod 755 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]