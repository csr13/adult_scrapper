#!/bin/bash

settings=config.production.settings

cd /src

python manage.py makemigrations --settings=$settings
python manage.py migrate --settings=$settings
python manage.py collectstatic --no-input --settings=$settings
python manage.py create_su --settings=$settings
python manage.py initial_migration --settings=$settings

gunicorn --workers=2 \
    --threads=2 \
    --reload \
    --bind 0.0.0.0:6969 \
    --access-logfile - \
    config.production.wsgi:application

