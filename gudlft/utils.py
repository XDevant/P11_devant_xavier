from flask import request


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
