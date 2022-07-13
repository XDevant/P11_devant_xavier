from flask import Flask
from gudlft.config import BaseConfig
from gudlft.utils import load_data


def create_app(config_class=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['DB'] = load_data(app.config['DATABASE'])
    from gudlft import views
    app.register_blueprint(views.bp)
    return app
