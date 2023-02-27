import os

import lmserver.model

from flask import Flask, redirect


def create_app():
    app = Flask(__name__)
    #app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py') #, silent=True)

    print(app.config['MODEL'])
    app.model = model.load(app.config['MODEL'])
    
    from . import view
    app.register_blueprint(view.bp)

    @app.route('/')
    def root_redirect():
        return redirect('lmserver')

    return app
