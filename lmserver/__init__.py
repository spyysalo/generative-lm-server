import os
import json

import lmserver.model

from flask import Flask, redirect


def load_examples(fn):
    examples = []
    with open(fn) as f:
        for l in f:
            examples.append(json.loads(l))
    return examples


def create_app():
    app = Flask(__name__)
    #app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py') #, silent=True)

    app.examples = load_examples(app.config['EXAMPLES'])

    app.model = lmserver.model.setup(app.config['MODEL'])

    from . import view
    app.register_blueprint(view.bp)

    @app.route('/')
    def root_redirect():
        return redirect('lmserver')

    return app
