from os import listdir, getcwd
from os.path import join, isfile, abspath,dirname
from werkzeug.utils import secure_filename
from flask import Blueprint, abort, json, request, redirect, flash, url_for
import numpy as np
import matplotlib.pyplot as plt
import wave
from pydub import AudioSegment
import sqlite3
import uuid

upload_api = Blueprint('upload_api', __name__)
clips_dir = join(dirname(abspath(__file__)),"..\\..\\database\\sounds\\")
thumb_dir = join(dirname(abspath(__file__)),"..\\..\\database\\thumbnails\\")
db_file = join(dirname(abspath(__file__)),"..\\..\\database\\database.db")



ALLOWED_EXTENSIONS = ['ogg']

## Helper
def get_db_connection():
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and \
            filename not in [f for f in listdir(clips_dir) if isfile(join(clips_dir, f))] and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_thumbnail(filename):
    sound = AudioSegment.from_ogg(join(clips_dir,filename))
    sound.export("temp.wav", format='wav')

    signal_wave = wave.open('temp.wav','r')
    sample_rate = signal_wave.getframerate()
    print(sample_rate)
    sig = signal_wave.readframes(-1)
    sig = np.fromstring(sig,dtype=np.int32)

    fig = plt.figure(figsize=(3,2))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    ax.margins(x=0, tight=False)
    fig.add_axes(ax)

    plt.plot(sig, color='#d94747', linewidth=2.5)
    print(thumb_dir,filename.split('.')[0])
    plt.savefig(join(thumb_dir,filename.split('.')[0]), bbox_inches=0, pad_inches=0, transparent=True)



@upload_api.route('/api/v1/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        title = request.form['title']
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
            sound_uuid = uuid.uuid4().hex
            sound_uri = secure_filename(sound_uuid +'.'+ file.filename.rsplit('.', 1)[1].lower())
            thumb_uri = sound_uuid + '.png'
            file.save(join(clips_dir, sound_uri))
            generate_thumbnail(sound_uri)

            conn = get_db_connection()
            conn.execute('INSERT INTO sounds (title, sound_uri, thumb_uri) VALUES (?, ?, ?)', (title, sound_uri, thumb_uri))
            conn.commit()
            conn.close()

            return redirect(url_for('upload_api.upload_file', name=sound_uri))
    return redirect('/')
