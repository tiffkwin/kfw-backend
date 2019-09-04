#################
#### imports ####
#################
 
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

################
#### config ####
################
 
app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/tiff/GitHub/kfw-backend/test.db'
db = SQLAlchemy(app)

from .models import TextFile

db.create_all()
 
####################
#### blueprints ####
####################
 
# from kfw-backend.services import file_blueprint
 
# register the blueprints
# app.register_blueprint(file_blueprint)