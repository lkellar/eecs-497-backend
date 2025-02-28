import flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_cors import CORS

class Base(DeclarativeBase):
    pass
    
db = SQLAlchemy(model_class=Base)

login_manager = LoginManager()

app = flask.Flask(__name__)

if app.debug:
    # disable cors restrictions when on debug mode
    CORS(app, supports_credentials=True)
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['REMEMBER_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True

app.config.from_object('backend.config')
db.init_app(app)
login_manager.init_app(app)

import backend.routes
import backend.models
from backend.models import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()