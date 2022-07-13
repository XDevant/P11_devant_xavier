from flask import Config


class BaseConfig(Config):
    SECRET_KEY = 'top-secret-key'
    JSONIFY_PRETTYPRINT_REGULAR = True
    DATABASE = "./gudlft/JSON/"
    TESTING = False
    LIVESERVER_PORT = '5000'
