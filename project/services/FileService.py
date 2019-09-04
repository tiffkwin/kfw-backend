import os
from werkzeug.utils import secure_filename
from .. import app
from ..models.TextFile import TextFile
from .. import db

# UPLOAD_FOLDER = './project/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def saveFile(file):
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        new_file = TextFile(user_id=1, file_path=filepath)
        print(new_file.file_path, new_file.user_id, new_file.file_id)
        db.session.add(new_file)
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True