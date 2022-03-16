from os import listdir, getcwd
from os.path import join, isfile, abspath,dirname
from werkzeug.utils import secure_filename
from flask import Blueprint, abort, json, request, redirect, flash, url_for

upload_api = Blueprint('upload_api', __name__)
clips_dir = join(dirname(abspath(__file__)),"..\\..\\database\\sounds\\")


ALLOWED_EXTENSIONS = ['ogg']

def allowed_file(filename):
    return '.' in filename and \
            filename not in [f for f in listdir(clips_dir) if isfile(join(clips_dir, f))] and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_api.route('/api/v1/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(join(clips_dir, filename))
            return redirect(url_for('upload_api.upload_file', name=filename))
    return redirect('/')
