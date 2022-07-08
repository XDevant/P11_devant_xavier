import json
from flask import Flask, render_template, request, redirect, flash, url_for


SETTINGS = {
    "clubs_filename": "clubs",
    "competitions_filename": "competitions"
}


def load_clubs(filename=SETTINGS["clubs_filename"]):
    with open(filename + '.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions(filename=SETTINGS["competitions_filename"]):
    with open(filename + '.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


def save_clubs(club_list, filename=SETTINGS["clubs_filename"]):
    with open(filename + '.json', 'w') as c:
        json.dump({'clubs': club_list}, c)
        return True


def save_competitions(competition_list, filename=SETTINGS["competitions_filename"]):
    with open(filename + '.json', 'w') as c:
        json.dump({'competitions': competition_list}, c)
        return True


def find_index_by_name(name, list_of_dicts):
    for i in range(len(list_of_dicts)):
        if list_of_dicts[i]['name'] == name:
            return i
    return -1


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()
for comp in competitions:
    if 'orders' not in comp.keys():
        comp['orders'] = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club_list = [club for club in clubs if club['email'] == request.form['email']]
    if len(club_list) > 0:
        return render_template('welcome.html', club=club_list[0], competitions=competitions)
    else:
        return redirect('/')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_clubs = [c for c in clubs if c['name'] == club]
    found_competitions = [c for c in competitions if c['name'] == competition]
    if len(found_clubs) > 0 and len(found_competitions) > 0:
        return render_template('booking.html', club=found_clubs[0], competition=found_competitions[0])
    elif len(found_clubs) > 0:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Something went wrong-please log again")
        return redirect('/index')


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    club_id = find_index_by_name(request.form['club'], clubs)
    club = clubs[club_id]
    competition_id = find_index_by_name(request.form['competition'], competitions)
    competition = competitions[competition_id]
    places_required = int(request.form['places'])
    places_available = int(competition['numberOfPlaces'])
    already_ordered = 0

    if club["name"] in competition['orders'].keys():
        already_ordered = competition['orders'][club["name"]]
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
        clubs[club_id] = club
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        competition['orders'][club["name"]] = already_ordered + places_required
        competitions[competition_id] = competition
        save_clubs(clubs)
        save_competitions(competitions)
        flash(f'Great-booking complete! ({places_required} places)')
        return render_template('welcome.html', club=club, competitions=competitions)
    return render_template('booking.html', club=club, competition=competition)


@app.route('/ranking')
def ranking():
    return render_template('ranking.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


# TODO:
"""
Invalid email blocks the app
"""
