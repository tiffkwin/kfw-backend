import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, Response, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Length
from project.services.FileService import *
from project import app
from project.services.MPService import *
from project.services.NADHService import *
from project.services.H2O2Service import *
import json

UPLOAD_FOLDER = './project/uploads'
OUTPUT_FOLDER = os.getcwd() + '/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# app = Flask(__name__)
# import 

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


@app.route('/', methods=['GET', 'POST'])
def findVenue():
    return render_template('upload.html')

@app.route('/test', methods=['POST'])
def test():
    try:
        data = json.loads(request.data)
        print(data)
        print(data['fname'])
        print(data['lname'])
        return Response('success', status=200)
    except Exception as e:
        print(e)
        return Response(e, status=500)

@app.route('/file_upload', methods=['GET'])
def fileUpload():
    return render_template('file_upload.html')

@app.route('/membrane_potential', methods=['GET'])
def mpAnalysis():
    return render_template('membrane_potential.html')

@app.route('/nadh', methods=['GET'])
def nadhAnalysis():
    return render_template('nadh.html')

@app.route('/h2o2', methods=['GET'])
def h2o2Analysis():
    return render_template('h2o2.html')

# @app.route('/download', methods=['GET'])
# def downloadResults():
#     return render_template('download.html')
    
@app.route('/upload', methods=['POST'])
def upload_file():
    # experiment_id = request.
    file = request.files['file']
    res = saveFile(file, request.form['experiment_id']) # FileService.py

    if res == True:
        return render_template('choose_assay.html')
    else:
        return render_template('upload_error.html')
    # return redirect(url_for('uploaded_file',filename=filename))

@app.route('/output/<experiment_id>', methods=['GET'])
def uploaded_file(experiment_id):
    # filename = request.args.get('filename')
    return send_from_directory(app.config['OUTPUT_FOLDER'], experiment_id + '.xlsx')

@app.route('/analyzeMP', methods=['POST'])
def analyze_mp():
    try:
        data = json.loads(request.data)

        std_curve = data['std_curve']
        slope = data['slope']
        y_int = data['y_int']
        substrates_list = data['substrates_list']
        experiment_id = data['experiment_id']
        sub_repetitions = data['sub_repetitions']
        additions_list = data['additions_list']
        group_descriptions = data['group_descriptions']
        times = data['times']

        res = analyzeMP(std_curve, slope, y_int, substrates_list, experiment_id, sub_repetitions, additions_list, group_descriptions, times)

        if res == True:
            # return render_template('download.html', experiment_id=experiment_id)
            return Response('success', status=200)
        else:
            return Response('error', status=500)
    except Exception as e:
        print(e)
        return Response('error', status=500)

@app.route('/analyzeNADH', methods=['POST'])
def analyze_nadh_redox():
    data = json.loads(request.data)

    substrates_list = data['substrates_list']
    experiment_id = data['experiment_id']
    sub_repetitions = data['sub_repetitions']
    additions_list = data['additions_list']
    group_descriptions = data['group_descriptions']
    times = data['times']

    res = analyzeNADHRedox(substrates_list, experiment_id, sub_repetitions, additions_list, group_descriptions, times)

    if res == True:
        return Response('success', status=200)
    else:
        return Response('error', status=500)

@app.route('/analyzeH2O2', methods=['POST'])
def analyze_h2o2():
    data = json.loads(request.data)

    slope_atp = data['slope_atp']
    y_int_atp = data['y_int_atp']
    slope_h2o2 = data['slope_h2o2']
    y_int_h2o2 = data['y_int_h2o2']
    mito_atp = data['mito_atp']
    mito_h2o2 = data['mito_h2o2']
    substrates_list = data['substrates_list']
    experiment_id = data['experiment_id']
    sub_repetitions = data['sub_repetitions']
    additions_list = data['additions_list']
    group_descriptions = data['group_descriptions']
    times = data['times']

    res = analyzeH2O2(slope_atp, y_int_atp, slope_h2o2, y_int_h2o2, substrates_list, mito_atp, mito_h2o2, experiment_id, sub_repetitions, additions_list, group_descriptions, times)

    if res == True:
        return Response('success', status=200)
    else:
        return Response('error', status=500)

if __name__ == "__main__":
    app.run()