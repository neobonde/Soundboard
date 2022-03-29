from os import listdir, getcwd, remove
from os.path import join, isfile, abspath,dirname
from werkzeug.utils import secure_filename
from flask import Blueprint, abort, json, request, redirect, flash, url_for
import numpy as np
import matplotlib.pyplot as plt
import wave
from pydub import AudioSegment
import sqlite3
import uuid
from pathlib import Path


upload_api = Blueprint('upload_api', __name__)
clips_dir = Path(dirname(abspath(__file__)),"../../database/sounds/")
thumb_dir = Path(dirname(abspath(__file__)),"../../database/thumbnails/")
db_file = Path(dirname(abspath(__file__)),"../../database/database.db")

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

@upload_api.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """

    print(r)
    print("Hello headers")

    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    # r.headers['Cache-Control'] = 'public, max-age=0'
    return r



@upload_api.route('/api/v1/upload', methods=['POST'])
def upload_sound():
    if request.method == 'POST':
        title = request.form['title']
        # check if the post request has the file part
        if 'file' not in request.files:
            return {'response':'No file selected'}, 400

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return {'response':'No file selected'}, 400

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

        else:
            return {'response':'Unsupported file format, only accepts .OGG'}, 415


            return redirect(url_for('upload_api.upload_file', name=sound_uri))
    return '', 204

@upload_api.route('/api/v1/rename', methods=['POST'])
def rename_sound():
    data = {}

    try:
        data = json.loads(request.data)
    except Exception:
        try:
            data = request.form.to_dict(flat=True)
        except:
            return  {'response':"Request body or form missing"}, 400

    soundId = None
    newName = ""

    if "sound" not in data:
        return  {'response':"No sound specified to edit"}, 400
    soundId = data["sound"]

    if "new_name" not in data:
        return  {'response':"No new name specified, cannot rename"}, 400
    newName = data["new_name"]


    conn = get_db_connection()
    conn.execute(f"UPDATE sounds SET title = '{newName}' WHERE id={soundId}")
    conn.commit()
    conn.close()

    return  {'response':'Sound renamed'}, 202


@upload_api.route('/api/v1/delete', methods=['POST'])
def delete_sound():
    data = {}

    try:
        data = json.loads(request.data)
    except Exception:
        try:
            data = request.form.to_dict(flat=True)
        except:
            return  {'response':"Request body or form missing"}, 400

    print(data)

    if "sound" in data:
        soundId = data["sound"]

        conn = get_db_connection()
        try:
            soundUri = conn.execute(f'SELECT sound_uri FROM sounds WHERE id={soundId}').fetchone()[0]
            thumbUri = conn.execute(f'SELECT thumb_uri FROM sounds WHERE id={soundId}').fetchone()[0]
            conn.execute(f'DELETE FROM sounds WHERE id={soundId}')
        except TypeError:
            conn.commit()
            conn.close()
            return  {'response':'File not found'}, 404

        conn.commit()
        conn.close()

        try:
            remove(Path(clips_dir, soundUri))
            remove(Path(thumb_dir, thumbUri))
        except FileNotFoundError:
            # It is Ok if the files have already been deleted
            pass

        return  {'response':'sound deleted'}, 200


    else:
        return  {'response':'No sound specified to delete'}, 400
