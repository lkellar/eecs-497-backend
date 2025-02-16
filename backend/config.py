import os

SQLALCHEMY_DATABASE_URI = os.environ.get('EECS497_BACKEND_DB_URI', 'postgresql+psycopg://localhost:5432/eecs497_backend')
# this must be defined externally
SECRET_KEY = os.environ['EECS497_BACKEND_SECRET_KEY']