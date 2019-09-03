#################
#### imports ####
#################
 
from flask import Flask
from flask_cors import CORS
 
 
################
#### config ####
################
 
app = Flask(__name__)
cors = CORS(app)
 
####################
#### blueprints ####
####################
 
# from kfw-backend.services import file_blueprint
 
# register the blueprints
# app.register_blueprint(file_blueprint)