from os import listdir, getcwd
from os.path import join, isfile, abspath,dirname
from flask import Blueprint, abort, json, request
import subprocess
import schedule



tv_api = Blueprint('tv_api', __name__)

def tv_on():
    command = "echo 'on 0' | cec-client -s -d 1"
    process = subprocess.run(command, shell=True, check=True)

def tv_off():
    command = "echo 'standby 0' | cec-client -s -d 1"
    process = subprocess.run(command, shell=True, check=True)

@tv_api.route('/api/v1/tv_on',methods=['POST'])
def tv_on_route():
    print("tv_on")
    tv_on()
    return json.dumps({"success": True}), 201

@tv_api.route('/api/v1/tv_off',methods=['POST'])
def tv_off_route():
    print("tv_off")
    tv_off()
    return json.dumps({"success": True}), 201


def setTvSchedule(onTime="08:00", offTime="15:44", days=["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"]):
    # Turn on and off tv on schedule

    print(f"Scheduling tv to turn on at: {onTime} and turn off at {offTime} on the days: {days}")

    if "MONDAY" in (day.upper() for day in days):
        schedule.every().monday.at(onTime).do(tv_on)
        schedule.every().monday.at(offTime).do(tv_off)

    if "TUESDAY" in (day.upper() for day in days):
        schedule.every().tuesday.at(onTime).do(tv_on)
        schedule.every().tuesday.at(offTime).do(tv_off)

    if "WEDNESDAY" in (day.upper() for day in days):
        schedule.every().wednesday.at(onTime).do(tv_on)
        schedule.every().wednesday.at(offTime).do(tv_off)

    if "THURSDAY" in (day.upper() for day in days):
        schedule.every().thursday.at(onTime).do(tv_on)
        schedule.every().thursday.at(offTime).do(tv_off)

    if "FRIDAY" in (day.upper() for day in days):
        schedule.every().friday.at(onTime).do(tv_on)
        schedule.every().friday.at(offTime).do(tv_off)

    if "SATURDAY" in (day.upper() for day in days):
        schedule.every().saturday.at(onTime).do(tv_on)
        schedule.every().saturday.at(offTime).do(tv_off)

    if "SUNDAY" in (day.upper() for day in days):
        schedule.every().sunday.at(onTime).do(tv_on)
        schedule.every().sunday.at(offTime).do(tv_off)
