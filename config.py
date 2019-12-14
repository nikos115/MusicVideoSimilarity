import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:pg#docker@localhost:5432/mvsimilarity"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
