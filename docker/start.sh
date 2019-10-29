#!/bin/bash

set -e

while ! (timeout 3 bash -c "</dev/tcp/${DB_HOST}/${DB_PORT}") &> /dev/null;
do
    echo waiting for PostgreSQL to start...;
    sleep 3;
done;
sleep 10;

./manage.py makemigrations --merge  --no-input --traceback
./manage.py migrate  --no-input --traceback
./manage.py collectstatic --no-input --traceback


if [ $DEBUG == '1' ]
then
   ./manage.py runserver 0.0.0.0:8000
else
  gunicorn -c docker/gunicorn_settings.py core.wsgi --access-logfile ../access.log --error-logfile ../error.log --log-level debug --log-config ./docker/gunicron-log.conf
fi
