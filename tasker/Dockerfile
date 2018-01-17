FROM python:3.6

RUN mkdir /tasker && mkdir /tasker/static && mkdir /tasker/data && mkdir /tasker/data/media
WORKDIR /tasker

RUN apt-get update && apt-get install -y unzip supervisor postgresql-dev g++ python3-dev openldap-clients openldap-dev openssl-dev libffi-dev freetds-dev unixodbc-dev tzdata
RUN pip install -q -U pip setuptools wheel

COPY /opt/asdd/instantclientlite121.zip /tasker/instantclientlite121.zip
COPY ../backend/requirements.txt requirements.txt

RUN mdir oic && cd oic && unzip ../instantclientlite121.zip
ENV LD_LIBRARY_PATH /tasker/oic:$LD_LIBRARY_PATH

RUN pip --no-cache-dir -r requirements.txt && pip install cx_Oracle

ENV DJANGO_SETTINGS_MODULE genisys.settings.tasker

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY ../backend/db/ /tasker/app/db/
COPY ../backend/esi/ /tasker/app/esi/
COPY ../backend/genisys/ /tasker/app/genisys/
COPY ../backend/manage.py /tasker/app/manage.py

VOLUME ["/tasker/data"]

ENTRYPOINT ["python", "/tasker/server.py"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
