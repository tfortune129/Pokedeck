# initialization of our app:

from flask import Flask
from config import Config

app = Flask(__name__)
#instance of a flask app
app.config.from_object(Config)


from . import routes