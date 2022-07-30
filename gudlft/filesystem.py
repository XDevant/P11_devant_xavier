import json
from flask import current_app


SETTINGS = {
    "tables": {
              "clubs": "clubs",
              "competitions": "competitions",
              "bookings": "bookings"
              }
}


def load_file(filename, path=None):
    if path is None:
        path = current_app.config['DATABASE'] + '/'
    else:
        path = path
    with open(path + filename + '.json') as c:
        new_list = json.load(c)[filename]
        return new_list


def load_data(path=None):
    db = {}
    for key, value in SETTINGS["tables"].items():
        db[key] = load_file(value, path)
    return db


def save_to_file(name, table):
    try:
        path = current_app.config['DATABASE'] + '/'
    except Exception:
        path = './test/Temp/'
    with open(path + name + '.json', 'w') as c:
        json.dump({name: table}, c, indent=4)
        return True


def save_data(db):
    for key, value in db.items():
        save_to_file(SETTINGS["tables"][key], value)
