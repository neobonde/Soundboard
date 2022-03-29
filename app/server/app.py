from operator import truediv
from .frontend import simple_page
from .api import sound_api, upload_api, tv_api, setTvSchedule
# from .api import tv_api
from flask import Flask


def run():
    app = Flask(__name__, static_folder = '../database/thumbnails')
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    app.register_blueprint(simple_page)
    app.register_blueprint(sound_api)
    app.register_blueprint(upload_api)
    app.register_blueprint(tv_api)

    setTvSchedule(onTime="08:00", offTime="15:44", days=["monday", "tuesday", "wednesday", "thursday", "friday"])

    app.run(host="0.0.0.0",port=8080, threaded=True)
