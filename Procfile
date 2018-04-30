web: gunicorn config.wsgi:application
worker: celery worker --app=medicalboard.taskapp --loglevel=info
