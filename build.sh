#!/usr/bin/env bash

set -o errexit  # Exit on any error

# Install the dependencies from requirements.txt
pip install -r requirements.txt

# Collect static files (this is necessary for deployment)
python manage.py collectstatic --no-input

# Apply migrations to the database
python manage.py migrate

# (Optional) You may want to restart your web server (e.g., Gunicorn or your deployment platform)
# Example for Gunicorn: 
# sudo systemctl restart gunicorn

# (Optional) Run any other tasks (e.g., starting the application)
# python manage.py runserver
