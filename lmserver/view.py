import requests

import lmserver.model

from flask import Blueprint
from flask import request, url_for, render_template, jsonify, make_response
from flask import current_app as app


bp = Blueprint('view', __name__, static_folder='static', url_prefix='/lmserver')


@bp.route('/')
def root():
    return show_index()


@bp.route('/')
def show_index():
    return render_template('index.html')


@bp.route('/generate', methods=['GET', 'POST'])
def tag_text():
    text = str(request.values['text'])
    format_ = str(request.values.get('format', 'html'))
    generation = lmserver.model.generate(app.tokenizer, app.model, text)
    print(generation)
    return render_template('index.html', **locals())
