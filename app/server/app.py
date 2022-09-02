from operator import truediv
import threading
from .frontend import simple_page
from .api import sound_api, upload_api, tv_api, setTvSchedule, tv_scheduler
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

    threading.Thread(target=lambda: app.run(host="0.0.0.0",port=8080, threaded=True, debug=False)).start()
    threading.Thread(target=lambda: tv_scheduler()).start()




    # app.run(host="0.0.0.0",port=8080, threaded=True, debug=False)
