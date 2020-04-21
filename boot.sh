#!/bin/sh
source venv/bin/activate
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - -k eventlet -w 1 server:app
