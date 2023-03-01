import requests

import lmserver.model

from logging import warning

from flask import Blueprint
from flask import request, url_for, render_template, jsonify, make_response
from flask import current_app as app


bp = Blueprint('view', __name__, static_folder='static', url_prefix='/lmserver')


@bp.route('/')
def root():
    return show_index()


@bp.route('/generate', methods=['GET', 'POST'])
def show_index():
    try:
        prompt = str(request.values['text'])
        prompt = prompt.replace('\r\n', '\n')
    except:
        prompt = ""
    try:
        length = int(request.values['length'])
    except:
        length = 10
    try:
        temperature = float(request.values['temperature'])
    except:
        temperature =  0.7
    if not prompt:
        generation = ""
    else:
        generation = app.model.generate(
            prompt,
            temperature=temperature,
            new_tokens=length,
        )
        if generation.startswith(prompt):
            generation = generation[len(prompt):]
        else:
            warning(f'MISMATCH:\n"{repr(prompt)}"\n"{repr(generation)}"')
            prompt = ''
    model_name = app.model.name
    return render_template('index.html', **locals())
