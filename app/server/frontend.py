from flask import Blueprint, render_template, abort, send_from_directory, json
from jinja2 import TemplateNotFound
from os.path import join, splitext
from .api.sound_api import get_files as get_effects


simple_page = Blueprint('simple_page', __name__, template_folder='../www/templates/', static_folder='../www/static/')

@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        effects_json, _ = get_effects()
        effects = json.loads(effects_json)
        effects = [splitext(x)[0] for x in effects]

        return render_template(f'{page}.html',effects=effects)
    except TemplateNotFound:
        abort(404)

@simple_page.route('/favicon.ico')
def favicon():
    return send_from_directory(join(simple_page.static_folder,'ico'),'favicon.ico',mimetype='image/vnd.microsoft.icon')
