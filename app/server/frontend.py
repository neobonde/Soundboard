from email.policy import default
import sqlite3
from flask import Blueprint, redirect, render_template, abort, send_from_directory, json, send_file, url_for
from jinja2 import TemplateNotFound
from os.path import join, splitext, dirname, abspath, isfile
from .api.sound_api import get_sounds
import sqlite3
from pathlib import(Path)

thumb_dir = Path(dirname(abspath(__file__)),"../database/thumbnails/")


simple_page = Blueprint('simple_page', __name__, template_folder='../www/templates/', static_folder='../www/static/')

@simple_page.after_request
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


@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        effects, _ = get_sounds()
        return render_template(f'{page}.html',effects=effects)
    except TemplateNotFound:
        abort(404)


@simple_page.route('/thumbnail/', defaults={'image':'default.png'})
@simple_page.route('/thumbnail/<image>')
def thumbnail(image):
    thumbnail_file = join(thumb_dir,image)
    if not isfile(thumbnail_file):
        thumbnail_file = join(thumb_dir,"default.png")
    return send_file(thumbnail_file, mimetype='image/png')

@simple_page.route('/static/')
def static_redirect():
    return redirect('/')

@simple_page.route('/favicon.ico')
def favicon():
    return send_from_directory(simple_page.static_folder,'favicon.ico',mimetype='image/vnd.microsoft.icon')
