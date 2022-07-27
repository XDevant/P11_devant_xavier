from flask import render_template, request, redirect, flash, url_for, current_app, Blueprint
from gudlft.utils import shutdown_server, find_index_by_key_value, get_booking, set_booking
from gudlft.filesystem import save_data


bp = Blueprint('gudlft', __name__, url_prefix='')


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/showSummary', methods=['POST'])
def show_summary():
    data = current_app.config['DB']
    form = request.form
    if "email" in form.keys():
        club_id = find_index_by_key_value("email", form['email'], data["clubs"])
        if club_id < 0:
            try:
                shutdown_server()
            except RuntimeError:
                raise RuntimeError("Server did not shut down")
            return '<h1>Server shutting down...</h1>'
    else:
        club_id = find_index_by_key_value("name", form['club'], data["clubs"])
        if club_id < 0:
            return redirect(url_for('gudlft.index'))
    return render_template('welcome.html', club=data["clubs"][club_id], competitions=data["competitions"])


@bp.route('/book/<competition>/<club>')
def book(competition, club):
    data = current_app.config['DB']
    club_id = find_index_by_key_value("name", club, data["clubs"])
    if club_id == -1:
        flash("Something went wrong-please log again")
        return redirect('/index')
    club = data["clubs"][club_id]
    competition_id = find_index_by_key_value("name", competition, data["competitions"])
    if competition_id == -1:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=data["competitions"])
    competition = data["competitions"][competition_id]
    return render_template('booking.html', club=club, competition=competition)


@bp.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    data = current_app.config['DB']
    club_name = request.form['club']
    competition_name = request.form['competition']
    club_id = find_index_by_key_value("name", club_name, data["clubs"])
    club = data["clubs"][club_id]
    competition_id = find_index_by_key_value("name", competition_name, data["competitions"])
    competition = data["competitions"][competition_id]
    places_required = int(request.form['places'])
    places_available = int(competition['numberOfPlaces'])
    already_ordered = get_booking(competition_name, club_name, data)

    if places_required < 0:
        flash(f'You can only book a positive number of places!')
    elif places_required + already_ordered > 12:
        flash(f'You can not buy more than 12 places! You previously bought {already_ordered}')
    elif places_available < places_required:
        flash(f'Only {places_available} places left, you asked {places_required}!')
    elif int(club["points"]) < places_required:
        flash(f'You have {club["points"]} points left, you asked {places_required} places!')
    else:
        club["points"] = int(club["points"]) - places_required
        data["clubs"][club_id] = club
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        data["competitions"][competition_id] = competition
        set_booking(competition_name, club_name, already_ordered + places_required, data)
        save_data(data)
        flash(f'Great-booking complete! ({places_required} places)')
        return render_template('welcome.html', club=club, competitions=data["competitions"])
    return render_template('booking.html', club=club, competition=competition)


@bp.route('/ranking')
def ranking():
    data = current_app.config['DB']
    club = request.args.get("club")
    competition = request.args.get("competition")
    return render_template('ranking.html', clubs=data["clubs"], club=club, competition=competition)


@bp.route('/logout')
def logout():
    return redirect('/index')
"""
L'échange actuel de 1 point = 1 place de compétition a été amélioré de sorte que 3 points = 1 place de compétition.

❒ Il existe un scénario de test qui encapsule le problème et la solution.

Le repo est présentable quand : 

❒ Si l'erreur est signalée, l'utilisateur voit un message d'erreur (par exemple : “Désolé, ce courriel n'a pas été trouvé”).

 Le bogue se trouve à la ligne 29 dans server.py. Il suppose que vous aurez toujours une liste des éléments renvoyés.
"""