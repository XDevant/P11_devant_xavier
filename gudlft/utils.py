import json
from flask import request, current_app


SETTINGS = {
    "tables": {
              "clubs": "clubs",
              "competitions": "competitions",
              "bookings": "bookings"
              }
}


def load_file(filename, path=None):
    if path is None:
        path = current_app.config['DATABASE']
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
    path = current_app.config['DATABASE']
    with open(path + name + '.json', 'w') as c:
        json.dump({name: table}, c)
        return True


def save_data(db):
    for key, value in db.items():
        save_to_file(SETTINGS["tables"][key], value)


def find_index_by_key_value(key, name, list_of_dicts):
    for i in range(len(list_of_dicts)):
        if list_of_dicts[i][key] == name:
            return i
    return -1


def shutdown_server():
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if shutdown is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown()


def get_booking(competition, club, db):
    if competition not in db["bookings"].keys() or club not in db["bookings"][competition].keys():
        return 0
    return int(db["bookings"][competition][club])


def set_booking(competition, club, places, db):
    if competition not in db["bookings"].keys():
        db["bookings"][competition] = {}
    db["bookings"][competition][club] = str(places)
