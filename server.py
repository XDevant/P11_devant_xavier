import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


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
    club_name = request.form['club']
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == club_name][0]
    places_required = int(request.form['places'])
    places_available = int(competition['numberOfPlaces'])
    already_ordered = 0
    if club_name in competition['orders'].keys():
        already_ordered = competition['orders'][club_name]
    if places_required < 0:
        flash(f'You can only book a positive number of places!')
    elif places_required + already_ordered > 12:
        flash(f'You can not buy mora than 12 places!')
    elif places_available < places_required:
        flash(f'Only {places_available} places left, you asked {places_required}!')
    elif club["points"] < places_required:
        flash(f'You have {club["points"]} points left, you asked {places_required} places!')
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        competition['orders'][club_name] = already_ordered + places_required
        club["points"] = int(club["points"]) - places_required
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
"""enregistrer les reservation de places dans les concours
La saisie d'un courriel inconnu entraîne le blocage de l'application
"""
