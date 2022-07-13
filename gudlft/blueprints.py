from flask import Blueprint


login = Blueprint('login', __name__, url_prefix='/')
home = Blueprint('home', __name__, url_prefix='/showSummary')
