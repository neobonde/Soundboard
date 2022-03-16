from .frontend import simple_page
from .api import sound_api, upload_api, tv_api, setTvSchedule
# from .api import tv_api
from flask import Flask



def run():
    print("Hello World")

    app = Flask(__name__, static_folder = '../www/static/')

    app.register_blueprint(simple_page)
    app.register_blueprint(sound_api)
    app.register_blueprint(upload_api)
    app.register_blueprint(tv_api)


    setTvSchedule(onTime="08:00", offTime="15:44", days=["monday", "tuesday", "wednesday", "thursday", "friday"])

    app.run(host="0.0.0.0",port=80,debug=True)
