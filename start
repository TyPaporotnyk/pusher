#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

poetry run python manage.py migrate
poetry run python manage.py collectstatic --noinput
poetry run gunicorn config.wsgi --bind 0.0.0.0:5000 --workers 3 --log-level=debug --chdir=/app
