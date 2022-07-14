from flask import Config


class BaseConfig(Config):
    SECRET_KEY = 'top-secret-key'
    JSONIFY_PRETTYPRINT_REGULAR = True
    DATABASE = "./gudlft/JSON/"
    TESTING = False
    SERVER_PORT = '5000'


class TestConfig(Config):
    SECRET_KEY = 'top-secret-key'
    JSONIFY_PRETTYPRINT_REGULAR = True
    DATABASE = "./test/JSON/"
    TEMP = "./test/Temp/"
    TESTING = True
    SERVER_PORT = '8000'
