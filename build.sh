#!/usr/bin/env bash
set -euo pipefail

# install deps (Render also runs pip automatically for many apps; explicit is fine)
pip install -r requirements.txt

# collect static into STATIC_ROOT
python manage.py collectstatic --no-input

# apply migrations (optional here — see notes below)
python manage.py migrate --no-input

