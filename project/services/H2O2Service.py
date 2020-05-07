import os
from werkzeug.utils import secure_filename
from .. import app
from .FileService import * 
from .. import db
from .H2O2 import *
import numpy as np
import pandas as pd

# UPLOAD_FOLDER = './project/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def analyzeH2O2(slope_atp, y_int_atp, slope_h2o2, y_int_h2o2, substrates_list, mito_atp, mito_h2o2, experiment_id, sub_repetitions, additions_list, group_descriptions, times):

    setVariables(slope_atp, y_int_atp, slope_h2o2, y_int_h2o2, substrates_list, mito_atp, mito_h2o2, experiment_id, sub_repetitions, additions_list, group_descriptions, times)

    bool_stdcurve = True # only for testing

    file_path = TextFile.query.filter_by(experiment_id=experiment_id).first().file_path

    try:
        mac = True
        if platform == "win32":
            mac = False

        # bool_stdcurve = get_input()
        #print(bool_stdcurve)
        print('-----------------------------------------------')
        print("Loading...")

        # Retrieves all .txt files in the current working directory
        root = os.getcwd()
        print(root)

        path = file_path

        # if mac:
        #     path = root + '/project/uploads/*.txt'
        # else:
        #     path = root + '\project\\uploads\\*.txt'
    
        print(path)

        files = glob.glob(path)   

        file_num = 1

        print(files)

        if mac:
            if (os.path.isdir(root + '/output') == False):
                os.makedirs('output')
        else:
            if (os.path.isdir(root + '\output') == False):
                os.makedirs('output')

        # Loops through every .txt file found
        for name in files:
            print('Analyzing file ' + str(file_num) + '...')

            if mac:
                # Stores file name
                filename = name.split('/')[-1]
            else:
                filename = name.split('\\')[-1]

            # Removes file type from filename
            shortened_filename = filename.split('.')[0]
            if mac:
                output_dir = root +'/output'
            else:
                output_dir = root +'\output'

            if (os.path.isdir(output_dir) == False):
                if mac:
                    os.chdir(root + '/output')
                else:
                    os.chdir(root + '\output')
                os.makedirs(shortened_filename)
            if mac:
                os.chdir(root + '/project/uploads')
            else:
                os.chdir(root + '\project\\uploads')

            # Creates .xlsx file to output analyzed data to
            writer = pd.ExcelWriter(experiment_id + '.xlsx')

            # ----DATA READ-IN----

            #print(filename) #uncomment this line for debugging

            # Reads in the data from the csv and stores it as a dataframe
            fluor_raw = pd.read_csv(filename, sep='\t', skiprows=6, skipfooter=1, header=None, engine='python')

            atp = pd.DataFrame()

            for column in fluor_raw[fluor_raw.columns[:2]]:
                atp[column] = fluor_raw[column]
            
            fluor_raw = fluor_raw.drop(fluor_raw.columns[[0, 1]], axis=1) ###FIX STUFF

            os.chdir(output_dir)
            new_cols = []
            for col in fluor_raw.columns:
                new_cols.append(int(col)-2)

            fluor_raw.columns = new_cols
            # Plot raw data
            # plot1(fluor_raw, 'H2O2 Raw Data', 'H2O2 Raw.png')
            # plot1(atp, 'ATP Raw Data', 'ATP Raw.png')

            # Produces metadata
            metadata = prod_metadata(bool_stdcurve)

            # Exports metadata to .xlsx file
            metadata.to_excel(writer, ('Metadata'))

            # Gets column labels
            column_labels = []
            for i in range(0,len(fluor_raw.columns)):
                if(i % 2 == 0):
                    column_labels.append('X')
                else:
                    column_labels.append('Y')

            # ----EXPORT - RAW DATA----

            fluor = fluor_raw.copy()
            fluor_raw.columns = column_labels
            fluor_raw.to_excel(writer, ('H2O2 Raw Data'))

            column_labels_atp = []
            for i in range(0,len(atp.columns)):
                if(i % 2 == 0):
                    column_labels_atp.append('X')
                else:
                    column_labels_atp.append('Y')

            atp_xy = atp.copy()
            atp.columns = column_labels_atp
            atp.to_excel(writer, ('ATP Raw Data'))

            # ----SLOPES CALCULATION - RAW DATA----
            slope_df = calc_slopes(fluor, substrates_list[1:])
            slope_atp_df = calc_slopes(atp_xy, [substrates_list[0]])

            # ----EXPORT - SLOPES DATA----

            # Plots slopes data
            # plot2(slope_df, 'H2O2 Slopes Data', 'H2O2 Slopes.png')
            # plot2(slope_atp, 'ATP Slopes Data', 'ATP Slopes.png')

            slope_df.to_excel(writer, ('H2O2 Slopes Data'))
            slope_atp_df.to_excel(writer, ('ATP Slopes Data'))

            # ----CORRECTION - SLOPES DATA----
            slope_df = corrected(slope_df, mito_h2o2)
            slope_atp_df = corrected(slope_atp_df, mito_atp)

            # ----EXPORT - CORRECTED SLOPES DATA----

            # Plots corrected slopes data
            # plot2(slope_df, 'Corrected H2O2 Slopes Data', 'Corrected H2O2 Slopes.png')
            # plot2(slope_atp, 'Corrected ATP Slopes Data', 'Corrected ATP Slopes.png')

            slope_df.to_excel(writer, ('Corrected H2O2 Slopes'))
            slope_atp_df.to_excel(writer, ('Corrected ATP Slopes'))
            # ----MEMBRANE POTENTIAL STANDARD CURVE----
            if(bool_stdcurve):
                fluor = std_curve(fluor, y_int_h2o2, slope_h2o2)
                atp_xy = std_curve(atp_xy, y_int_atp, slope_atp)

                # Plots standard curve data
                # plot1(fluor, 'H2O2 Std Curve Data', 'H2O2 Std Curve.png')
                # plot1(atp_xy, 'ATP Std Curve', 'ATP Std Curve.png')

            # ----AVERAGES - STANDARD CURVE----
                slopes_stdcurve = calc_slopes(fluor, substrates_list[1:])
                slopes_stdcurve_atp = calc_slopes(atp_xy, [substrates_list[0]])

                # Plots averaged standard curve data
                # plot2(slopes_stdcurve, 'H2O2 Std Curve Slopes Data', 'H2O2 Std Curve Slopes.png')
                # plot2(slopes_stdcurve_atp, 'ATP Std Curve Slopes Data', 'ATP Std Curve Slopes.png')

                correct_slopes_stdcurve = slopes_stdcurve.copy()
                correct_slopes_stdcurve_atp = slopes_stdcurve_atp.copy()

                correct_slopes_stdcurve = corrected(correct_slopes_stdcurve, mito_h2o2)
                correct_slopes_stdcurve_atp = corrected(correct_slopes_stdcurve_atp, mito_atp)

                # Plots averaged standard curve data
                # plot2(correct_slopes_stdcurve, 'H2O2 Corrected Std Curve Slopes Data', 'H2O2 Corrected Std Curve Slopes.png')
                # plot2(correct_slopes_stdcurve_atp, 'ATP Corrected Std Curve Slopes Data', 'ATP Corrected Std Curve Slopes.png')

                # ----EXPORT---


            # Set column labels
            fluor.columns = column_labels
            atp_xy.columns = column_labels_atp

            if(bool_stdcurve):
                fluor.to_excel(writer,('H2O2 Std Curve'))
                slopes_stdcurve.to_excel(writer,('H2O2 Std Curve Slopes'))
                correct_slopes_stdcurve.to_excel(writer,('H2O2 Corrected Std Curve Slopes'))

                atp_xy.to_excel(writer, ('ATP Std Curve'))
                slopes_stdcurve_atp.to_excel(writer,('ATP Std Curve Slopes'))
                correct_slopes_stdcurve_atp.to_excel(writer,('ATP Corrected Std Curve Slopes'))

            # Saves excel file and moves on to next file to be analyzed if there is one
            writer.save()
            file_num += 1
            os.chdir(root)

        print('Analysis complete')
        print('-----------------------------------------------')
        return True
    except Exception as e:
        print(e)
        return False
