import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, Response
from project.services.FileService import *
from project import app

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
    res = saveFile(file)

    if res == True:
        return Response('success', status=200)
    else:
        return Response('error', status=500)
    # return redirect(url_for('uploaded_file',filename=filename))

@app.route('/uploads')
def uploaded_file():
    filename = request.args.get('filename')
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    