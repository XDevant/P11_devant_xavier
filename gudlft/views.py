from flask import render_template, request, flash, current_app, Blueprint
from gudlft.utils import find_index_by_key_value, get_booking, set_booking
from gudlft.filesystem import save_data

PLACE_COST = 3
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
    else:
        club_id = find_index_by_key_value("name", form['club'], data["clubs"])
    if club_id < 0:
        flash("Désolé, couriel non trouvé.")
        return render_template('index.html')
    return render_template('welcome.html', club=data["clubs"][club_id], competitions=data["competitions"])


@bp.route('/book/<competition>/<club>')
def book(competition, club):
    data = current_app.config['DB']
    club_id = find_index_by_key_value("name", club, data["clubs"])
    if club_id == -1:
        flash("Session expirée, veuillez vous reconnecter")
        return render_template('index.html')
    club = data["clubs"][club_id]
    competition_id = find_index_by_key_value("name", competition, data["competitions"])
    if competition_id == -1:
        flash("Ressource indisponible ou inexistante.")
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
        flash(f'Pour désinscrire des participants, contactez notre équipe!')
    elif places_required + already_ordered > 12:
        flash(f'Vous ne pouvez pas réserver plus de 12 places! vous en avez déjà {already_ordered}')
    elif places_available < places_required:
        flash(f'Plus que {places_available} places disponibles, vous en réservez {places_required}!')
    elif int(club["points"]) < places_required * PLACE_COST:
        flash(f"Vous n'avez que {club['points']} points, vous demandez {places_required} places!")
        flash(f"Rappel: chaque réservation coûte 3 point")
    else:
        club["points"] = int(club["points"]) - places_required * PLACE_COST
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
    return render_template('index.html')
