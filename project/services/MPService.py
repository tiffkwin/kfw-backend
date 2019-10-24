import os
from werkzeug.utils import secure_filename
from .. import app
from .FileService import * 
from .. import db
from .membrane_potential import *

# UPLOAD_FOLDER = './project/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def analyzeMP(slope, y_int, substrates_list, experiment_id, sub_repetitions, additions_list, group_descriptions):

    setVariables(slope, y_int, substrates_list, experiment_id, sub_repetitions, additions_list, group_descriptions)

    bool_stdcurve = True # only for testing

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

        if mac:
            path = root + '/project/uploads/*.txt'
        else:
            path = root + '\project\uploads\*.txt'
    
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
                output_dir = root +'/output/' + shortened_filename
            else:
                output_dir = root +'\output\\' + shortened_filename

            if (os.path.isdir(output_dir) == False):
                if mac:
                    os.chdir(root + '/output')
                else:
                    os.chdir(root + '\output')
                os.makedirs(shortened_filename)
            if mac:
                os.chdir(root + '/project/uploads')
            else:
                os.chdir(root + '\project\uploads')

            # Creates .xlsx file to output analyzed data to
            writer = pd.ExcelWriter(shortened_filename + '.xlsx')

            # ----DATA READ-IN----

            #print(filename) #uncomment this line for debugging

            # Reads in the data from the csv and stores it as a dataframe
            fluor_raw = pd.read_csv(filename, sep='\t', skiprows=6, skipfooter=1, header=None, engine='python')

            os.chdir(output_dir)

            # Plot raw data
            # plot1(fluor_raw, 'Raw Data', 'Raw.png')

            # Produces metadata
            metadata = prod_metadata(bool_stdcurve)
            print('prod metadata')

            # Exports metadata to .xlsx file
            metadata.to_excel(writer, ('Metadata'))
            print('meta to xl')

            # Gets column labels
            column_labels = []
            for i in range(0,len(fluor_raw.columns)):
                if(i % 2 == 0):
                    column_labels.append('X')
                else:
                    column_labels.append('Y')

            # ----EXPORT TO EXCEL - RAW DATA----
            print('raw to xl')
            fluor = fluor_raw.copy()
            fluor_raw.columns = column_labels
            fluor_raw.to_excel(writer, ('Raw Data'))

            # ----AVERAGES - RAW DATA----
            print('avg raw')
            avg_raw = averages(fluor)

            # Plots averaged raw data
            # plot2(avg_raw, 'Averaged Raw Data', 'Avg_Raw.png')

            # ----EXPORT TO EXCEL - AVG RAW DATA----
            print('raw avg to xl')
            avg_raw.to_excel(writer, ('Averaged Raw Data'))

            # Performs correction calculation
            print('correct raw')
            corrected_raw = corrected(avg_raw)

            # Plots corrected data
            # plot2(corrected_raw, 'Corrected Data', 'Corrected.png')

            # ----MEMBRANE POTENTIAL STANDARD CURVE----
            if(bool_stdcurve):
                fluor = std_curve(fluor)

                # Plots standard curve data
                # plot1(fluor, 'Standard Curve Data', 'Standard_Curve.png')

            # ----AVERAGES - STANDARD CURVE----

                avg_stdcurve = averages(fluor)

                # Plots averaged standard curve data
                # plot2(avg_stdcurve, 'Averaged Standard Curve Data', 'Avg_Standard_Curve.png')

            # ----EXPORT TO EXCEL - CORRECTED RAW DATA---

            # Set column labels
            fluor.columns = column_labels

            corrected_raw.to_excel(writer,('Corrected Raw Data'))

            # ----EXPORT TO EXCEL - STANDARD CURVE / AVERAGED STANDARD CURVE DATA---

            if(bool_stdcurve):
                fluor.to_excel(writer,('Standard Curve'))
                avg_stdcurve.to_excel(writer,('Averaged Standard Curve'))

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
