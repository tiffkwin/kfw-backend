from .. import db

class TextFile(db.Model):
    __tablename__ = 'textfile'

    file_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    file_path = db.Column(db.String(300), unique=False, nullable=False)
