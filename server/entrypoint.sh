#!/bin/sh

echo "Flask app started!"

# Run below commands from manage.py to initialize db and have some default data.
uwsgi --ini /etc/uwsgi.ini
