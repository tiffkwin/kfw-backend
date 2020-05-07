#################
#### imports ####
#################
 
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

################
#### config ####
################
 
app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/tiff/GitHub/kfw-backend/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

from .models import TextFile

db.create_all()
 
####################
#### blueprints ####
####################
 
# from kfw-backend.services import file_blueprint
 
# register the blueprints
# app.register_blueprint(file_blueprint)