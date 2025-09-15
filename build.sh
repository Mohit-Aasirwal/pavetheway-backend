#!/bin/sh
set -eu
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py create_admin
