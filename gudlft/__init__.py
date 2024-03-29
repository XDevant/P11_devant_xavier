from flask import Flask
from gudlft.config import BaseConfig, TestConfig
from gudlft.filesystem import load_data


def create_app(config_class=BaseConfig, test_config_class=TestConfig, testing=True):
    app = Flask(__name__)
    if testing:
        app.config.from_object(test_config_class)
    else:
        app.config.from_object(config_class)
    if 'DB' not in app.config.keys():
        with app.app_context():
            app.config['DB'] = load_data()
    if testing:
        app.config['DATABASE'] = './test/Temp'
    from gudlft import views
    app.register_blueprint(views.bp)
    return app
