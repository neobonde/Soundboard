from os import listdir, getcwd
from os.path import join, isfile, abspath,dirname
from flask import Blueprint, abort, json, request, send_file, jsonify
from pygame import mixer
import sqlite3
from pathlib import Path

sound_api = Blueprint('sound_api', __name__)

clips_dir = Path(dirname(abspath(__file__)), "../../database/sounds/")
db_file = Path(dirname(abspath(__file__)), "../../database/database.db")

nextChannel = 0

#Helper
def init_mixer():
    if not mixer.get_init():
        mixer.init()
        mixer.set_num_channels(10)

def get_db_connection():
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    return conn

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@sound_api.after_request
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

@sound_api.route('/api/v1/get-sounds',methods=['GET'])
def get_sounds():
    conn = get_db_connection()
    conn.row_factory = dict_factory
    sounds = conn.execute('SELECT * FROM sounds ORDER BY title ASC').fetchall()
    conn.close()

    return jsonify(sounds), 200


@sound_api.route('/api/v1/play',methods=['POST','GET'])
def play():

    init_mixer()
    global nextChannel
    data = {}

    print("========")
    print("\tRequestee: " + request.remote_addr)

    try:
        data = json.loads(request.data)
    except Exception:
        try:
            data = request.form.to_dict(flat=True)
        except:
            return json.dumps({"error": "Request body or form missing"}), 400

    if "volume" in data:
        mixer.Channel(nextChannel).set_volume((int(data['volume']))/100)
        print("\tVolume: " + data['volume'] + "%")

    else:
        mixer.Channel(nextChannel).set_volume(50)
        print("\tVolume: 50%" )

    if "sound" in data:
        file = data["sound"]
        if "." in file:
            if not file.endswith(".ogg"):
                name, format = file.split(".")
                return json.dumps({"error": "Unsupported format " + format, "supported_formats": ".ogg"}), 415
        else:
            file += ".ogg" # Assume .ogg

        if not isfile(Path(clips_dir, file)):
            print(Path(clips_dir, file))
            return json.dumps({"error": "File " + file + " not found"}), 404

        sound = mixer.Sound(Path(clips_dir, file))
        mixer.Channel(nextChannel).play(sound)
        old_channel = nextChannel
        nextChannel = (nextChannel + 1) % 10
        print("\tSound: "+file)

        return json.dumps({"success": True, "channel": old_channel}), 201

    return json.dumps({"error": "No sound reference found"}), 404


@sound_api.route('/api/v1/stop',methods=['POST'])
def stop():
    init_mixer()
    try:
        data = json.loads(request.data)
        if "channel" in data:
            mixer.Channel(data["channel"]).stop()
        else:
            for i in range(10):
                mixer.Channel(i).stop()
        return json.dumps({"success": True}), 201
    except:
        for i in range(10):
            mixer.Channel(i).stop()
        return json.dumps({"success": True}), 201
