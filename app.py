import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, Response
from project.services.FileService import *
from project import app
from project.services.MPService import *
import json

UPLOAD_FOLDER = './project/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# app = Flask(__name__)
# import 

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    res = saveFile(file) # FileService.py

    if res == True:
        return Response('success', status=200)
    else:
        return Response('error', status=500)
    # return redirect(url_for('uploaded_file',filename=filename))

@app.route('/uploads')
def uploaded_file():
    filename = request.args.get('filename')
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/analyzeMP', methods=['POST'])
def analyze_mp():
    data = json.loads(request.data)

    slope = data['slope']
    y_int = data['y_int']
    substrates_list = data['substrates_list']
    experiment_id = data['experiment_id']
    sub_repetitions = data['sub_repetitions']
    additions_list = data['additions_list']
    group_descriptions = data['group_descriptions']

    res = analyzeMP(slope, y_int, substrates_list, experiment_id, sub_repetitions, additions_list, group_descriptions)

    if res == True:
        return Response('success', status=200)
    else:
        return Response('error', status=500)

if __name__ == "__main__":
    app.run()