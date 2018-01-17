FROM python:3.5-alpine

RUN apk add -q --no-cache supervisor postgresql-dev g++ python3-dev musl-dev openldap-clients openldap-dev openssl-dev libffi-dev freetds freetds-dev libc-dev unixodbc-dev tzdata

RUN mkdir /backend
WORKDIR /backend

COPY entrypoint.sh /

ENTRYPOINT ["/entrypoint.sh"]

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

COPY requirements.txt /backend/
RUN pip install -q -U pip setuptools wheel
RUN pip install -q -r requirements.txt

ENV PYTHONUBUFFERED t
ENV DJANGO_SETTINGS_MODULE genisys.settings.development

COPY api/ /backend/api/
COPY genisys/ /backend/genisys/
COPY manage.py /backend/manage.py

