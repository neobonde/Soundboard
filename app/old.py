#!/usr/bin/env python
from operator import contains
from flask import Flask, json, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from os import listdir
from os.path import isfile, join, splitext
import time
from pygame import mixer
import subprocess
from multiprocessing import Process
import schedule


api = Flask(__name__, template_folder='.')
nextChannel = 0

clips_dir = "/home/pi/Music/audio-clips/"
api.config['UPLOAD_FOLDER'] = clips_dir
ALLOWED_EXTENSIONS = ['ogg']


def allowed_file(filename):
    return '.' in filename and \
            filename not in [f for f in listdir(clips_dir) if isfile(join(clips_dir, f))] and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route('/get-files',methods=['GET'])
def get_files():
    files = [f for f in listdir(clips_dir) if isfile(join(clips_dir, f))]
    return json.dumps(files), 201



@api.route('/play',methods=['POST','GET'])
def play():
    global nextChannel
    data = {}
    try:
        data = json.loads(request.data)
    except Exception:
        try:
            data = request.form.to_dict(flat=True)
        except:
            return json.dumps({"error": "Request body or form missing"}), 400

    if "volume" in data:

        mixer.Channel(nextChannel).set_volume((int(data['volume']))/100)
    else:
        mixer.Channel(nextChannel).set_volume(50)

    if "sound" in data:
        file = data["sound"]
        if "." in file:
            if not file.endswith(".ogg"):
                name, format = file.split(".")
                return json.dumps({"error": "Unsupported format " + format, "supported_formats": ".ogg"}), 415
        else:
            file += ".ogg" # Assume .ogg

        if not isfile(clips_dir + file):
            # print(clips_dir + file)
            return json.dumps({"error": "File " + file + " not found"}), 404

        sound = mixer.Sound(clips_dir + file)
        mixer.Channel(nextChannel).play(sound)
        old_channel = nextChannel
        nextChannel = (nextChannel + 1) % 10

        return json.dumps({"success": True, "channel": old_channel}), 201

    return json.dumps({"error": "No sound reference found"}), 404



@api.route('/stop',methods=['POST'])
def stop():
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



@api.route('/tv_on',methods=['POST'])
def tv_on_route():
    tv_on()
    return json.dumps({"success": True}), 201

def tv_on():
    command = "echo 'on 0' | cec-client -s -d 1"
    process = subprocess.run(command, shell=True, check=True)


@api.route('/tv_off',methods=['POST'])
def tv_off_route():
    tv_off()
    return json.dumps({"success": True}), 201

def tv_off():
    command = "echo 'standby 0' | cec-client -s -d 1"
    process = subprocess.run(command, shell=True, check=True)



@api.route('/')
def base():

    effects = [f for f in listdir(clips_dir) if isfile(join(clips_dir, f))]
    effects = [splitext(x)[0] for x in effects]

    return render_template('./index.htm', effects=sorted(effects))




@api.route('/upload', methods=['GET', 'POST'])
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
            file.save(join(api.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', name=filename))
    return redirect('/')

def tv_scheduler():
    while True:
        print("Checking schedule")
        schedule.run_pending()
        time.sleep(30)


if __name__ == '__main__':


    # Turn on and off tv on schedule
    schedule.every().monday.at("08:00").do(tv_on)
    schedule.every().tuesday.at("08:00").do(tv_on)
    schedule.every().wednesday.at("08:00").do(tv_on)
    schedule.every().thursday.at("08:00").do(tv_on)
    schedule.every().friday.at("08:00").do(tv_on)

    schedule.every().monday.at("15:44").do(tv_off)
    schedule.every().tuesday.at("15:44").do(tv_off)
    schedule.every().wednesday.at("15:44").do(tv_off)
    schedule.every().thursday.at("15:44").do(tv_off)
    schedule.every().friday.at("15:44").do(tv_off)


    p = Process(target=tv_scheduler)
    p.start()
    mixer.init()
    mixer.set_num_channels(10)
    api.run(host="0.0.0.0",port=8080)
    p.join()
