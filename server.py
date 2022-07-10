import json
from flask import Flask, render_template, request, redirect, flash, url_for


SETTINGS = {
    "tables": {
              "clubs": "clubs",
              "competitions": "competitions",
              "bookings": "bookings"
              },
    "path": "./JSON/"
}


def load_file(filename):
    path = SETTINGS['path']
    with open(path + filename + '.json') as c:
        new_list = json.load(c)[filename]
        return new_list


def load_data():
    db = {}
    for key, value in SETTINGS["tables"].items():
        db[key] = load_file(value)
    return db


def save_to_file(name, table):
    path = SETTINGS['path']
    with open(path + name + '.json', 'w') as c:
        json.dump({name: table}, c)
        return True


def save_data(db):
    for key, value in db.items():
        save_to_file(SETTINGS["tables"][key], value)


def find_index_by_name(name, list_of_dicts):
    for i in range(len(list_of_dicts)):
        if list_of_dicts[i]['name'] == name:
            return i
    return -1


def shutdown_server():
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if shutdown is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown()


def get_booking(competition, club, table):
    if competition not in table.keys() or club not in table[competition].keys():
        return 0
    return int(table[competition][club])


def set_booking(competition, club, places, table):
    if competition not in table.keys():
        table[competition] = {}
    else:
        table[competition][club] = str(places)


app = Flask(__name__)
app.secret_key = 'something_special'

data = load_data()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club_list = [club for club in data["clubs"] if club['email'] == request.form['email']]
    if len(club_list) > 0:
        return render_template('welcome.html', club=club_list[0], competitions=data["competitions"])
    else:
        try:
            shutdown_server()
        except RuntimeError:
            if not app.testing:
                raise RuntimeError("Server did not shut down")
        return '<h1>Server shutting down...</h1>'


@app.route('/book/<competition>/<club>')
def book(competition, club):
    club_id = find_index_by_name(club, data["clubs"])
    if club_id == -1:
        flash("Something went wrong-please log again")
        return redirect('/index')
    club = data["clubs"][club_id]
    competition_id = find_index_by_name(competition, data["competitions"])
    if competition_id == -1:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=data["competitions"])
    competition = data["competitions"][competition_id]
    return render_template('booking.html', club=club, competition=competition)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    club_name = request.form['club']
    competition_name = request.form['competition']
    club_id = find_index_by_name(club_name, data["clubs"])
    club = data["clubs"][club_id]
    competition_id = find_index_by_name(competition_name, data["competitions"])
    competition = data["competitions"][competition_id]
    places_required = int(request.form['places'])
    places_available = int(competition['numberOfPlaces'])
    already_ordered = get_booking(competition_name, club_name, data["bookings"])

    if places_required < 0:
        flash(f'You can only book a positive number of places!')
    elif places_required + already_ordered > 12:
        flash(f'You can not buy more than 12 places!')
    elif places_available < places_required:
        flash(f'Only {places_available} places left, you asked {places_required}!')
    elif int(club["points"]) < places_required:
        flash(f'You have {club["points"]} points left, you asked {places_required} places!')
    else:
        club["points"] = int(club["points"]) - places_required
        data["clubs"][club_id] = club
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        data["competitions"][competition_id] = competition
        set_booking(competition_name, club_name, already_ordered + places_required, data["bookings"])
        save_data(data)
        flash(f'Great-booking complete! ({places_required} places)')
        return render_template('welcome.html', club=club, competitions=data["competitions"])
    return render_template('booking.html', club=club, competition=competition)


@app.route('/ranking')
def ranking():
    return render_template('ranking.html', clubs=data["clubs"])


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
