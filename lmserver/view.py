import requests

import lmserver.model

from random import randint
from logging import warning

from flask import Blueprint
from flask import request, url_for, render_template, jsonify, make_response
from flask import current_app as app


bp = Blueprint('view', __name__, static_folder='static', url_prefix='/lmserver')


@bp.route('/')
def root():
    return generate()


@bp.route('/generate', methods=['GET', 'POST'])
def generate():
    try:
        prompt = str(request.values['text'])
        prompt = prompt.replace('\r\n', '\n')
    except:
        prompt = ""

    try:
        length = int(request.values['length'])
    except:
        length = 100

    try:
        temperature = float(request.values['temperature'])
    except:
        temperature =  0.7

    try:
        seed = int(request.values['seed'])
    except:
        seed = randint(0, 2**32)

    if not prompt:
        generation = ""
        model_name = None
        examples = app.examples
    else:
        generation = app.model.generate(
            prompt,
            temperature=temperature,
            new_tokens=length,
            seed=seed,
        )
        model_name = app.model.name
        examples = None
        if generation.startswith(prompt):
            generation = generation[len(prompt):]
        else:
            warning(f'MISMATCH:\n"{repr(prompt)}"\n"{repr(generation)}"')
            prompt = ''
    link = url_for(
        'view.generate',
        text=prompt,
        seed=seed,
        length=length,
        temperature=temperature
    )
    return render_template('index.html', **locals())
