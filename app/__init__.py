# initialization of our app:

from flask import Flask
from config import Config
from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager
# from flask_cors import CORS

# from .auth.routes import auth
# from .api.routes import api



app = Flask(__name__)
#instance of a flask app
app.config.from_object(Config)
# CORS(app)


db.init_app(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# app.register_blueprint(auth)
# app.register_blueprint(api)



from . import routes
from . import models