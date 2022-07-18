from flask import Config
from copy import deepcopy
from test.data import db


class BaseConfig(Config):
    SECRET_KEY = 'top-secret-key'
    JSONIFY_PRETTYPRINT_REGULAR = True
    DATABASE = "./gudlft/JSON/"
    TESTING = False
    PORT = '5000'


class TestConfig(Config):
    SECRET_KEY = 'top-secret-key'
    JSONIFY_PRETTYPRINT_REGULAR = True
    DATABASE = "./test/JSON/"
    TEMP = "./test/Temp/"
    TESTING = True
    PORT = '8000'


class PytestConfig(Config):
    SECRET_KEY = 'top-secret-key'
    JSONIFY_PRETTYPRINT_REGULAR = True
    TESTING = True
    DATABASE = "./test/JSON/"
    TEMP = "./test/Temp/"
    DB = deepcopy(db)
    PORT = '8001'
