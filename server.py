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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club_list = [club for club in clubs if club['email'] == request.form['email']]
    if len(club_list) > 0:
        return render_template('welcome.html', club=club_list[0], competitions=competitions)
    else:
        return redirect('/index')


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
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
