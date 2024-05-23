import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    #SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_SQLALCHEMY_DATABASE_URI')
    TESTING = True
