import os

basedir = os.path.abspath(os.path.dirname(__name__))

class Config():
    FLASK_APP = os.environ.get('FLASK_APP') # this is how you will run
    FLASK_ENV = os.environ.get('FLASK_ENV')