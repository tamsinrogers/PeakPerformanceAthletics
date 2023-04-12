'''THIS FILE (VIEWS.PY) WRITES CUSTOM DASHBOARD VIEWS FOR THE
ADMIN, COACH, & ATHLETE.  ALSO HANDLES UPLOADS + PERMISSIONS'''

from flask import (Blueprint, render_template, request,
                   flash, redirect, url_for, current_app)
from flask_login import login_required, login_user
from flask_security import current_user, auth_required
from .decorators import protect_athlete_view
from . import db
from .models import User, Role, parse_csv, Sleep, Nutrition, Readiness, Team
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import re
import pandas as pd
import string
from statistics import mean
from .plots import pie_chart, line_chart

views = Blueprint('views', __name__)


@views.route("/")
def home():
    '''Redirects to the appropriate page depending on user role
    (admin, coach, or athlete)'''
    return redirect(url_for('security.login'))


@views.route("/adminView")
@auth_required()
def adminView():
    '''Admin dashboard view: displays average values
    (sleep, nutrition, readiness) for all athletes across all teams.'''

    readinessQ = Readiness.query.filter(Readiness.ReadinessScore > 0)
    sleepQ = Sleep.query.filter(Sleep.TotalSleepScore > 0)
    nutritionQ = Nutrition.query.filter(Nutrition.calories > 0)

    readinessScores = ([readiness.ReadinessScore for readiness in readinessQ])
    sleepDurations = ([sleep.TotalSleepDuration for sleep in sleepQ])
    sleepScores = ([sleep.TotalSleepScore for sleep in sleepQ])
    cals = ([nutrition.calories for nutrition in nutritionQ])

    # READINESS GRAPH

    if len(readinessScores) > 0:
        readinessScore = round(mean(readinessScores), 1)
        readinessV = [readinessScore, (100-readinessScore)]
    else:
        readinessV = [0]

    readinessGraphJSON = pie_chart(readinessV, 'Readiness',
                                   ['Readiness Score'])

    # NUTRITION GRAPH
    if len(cals) > 0:
        calorie = round(mean(cals), 1)
        nutritionV = [calorie, (3000-calorie)]
    else:
        nutritionV = [0]

    nutritionGraphJSON = pie_chart(nutritionV, 'Nutrition',
                                   ['Nutrition Score'])

    # SLEEP GRAPH
    if len(sleepDurations) > 0:
        sleepDuration = round(mean(sleepDurations), 1)
        sleepV = [sleepDuration, (8-sleepDuration)]
    else:
        sleepV = [0]

    sleepGraphJSON = pie_chart(sleepV, 'Sleep', ['Sleep Score'])

    # LINE GRAPH
    timeStamp = []
    list = []

    if len(readinessScores) > 0:
        for item in readinessScores:
            list.append(item)
            timeStamp.append(readinessScores.index(item))
    else:
        timeStamp = [0]
        list = [0]

    teamGraphJSON = line_chart(timeStamp, list, 'Readiness History')

    list = User.query.all()
    teams = Team.query.all()
    teams_data = {}

    for team in teams:
        team_sleep = 0
        team_quality = 0
        team_readiness = 0
        team_calories = 0
        if len(team.users) != 0:
            athletes = {a for a in team.users if a.role == 'athlete'}

            for athlete in athletes:
                athlete_sleep = 0
                athlete_quality = 0
                athlete_readiness = 0
                athlete_calories = 0
                if len(athlete.sleep) != 0:
                    for sleep in athlete.sleep:
                        athlete_sleep += sleep.TotalSleepDuration
                        athlete_quality += sleep.TotalSleepScore

                    athlete_sleep = athlete_sleep/len(athlete.sleep)
                    athlete_quality = athlete_quality/len(athlete.sleep)
                if len(athlete.readiness) != 0:
                    for readiness in athlete.readiness:
                        athlete_readiness += readiness.ReadinessScore
                    athlete_readiness = athlete_readiness/len(
                                        athlete.readiness)
                else:
                    athlete_readiness = 0
                if len(athlete.nutrition) != 0:
                    for nutrition in athlete.nutrition:
                        athlete_calories += nutrition.calories
                    athlete_calories = athlete_calories/len(athlete.nutrition)
                else:
                    athlete_readiness = 0

                team_sleep += athlete_sleep
                team_quality += athlete_quality
                team_readiness += athlete_readiness
                team_calories += athlete_calories

            totPlayers = len(team.users)
            
            teams_data[team.name] = [round(team_sleep/totPlayers, 1),
                                     round(team_quality/totPlayers, 1),
                                     round(team_readiness/totPlayers, 1),
                                     round(team_calories/totPlayers, 1)]

        else:
            teams_data[team.name] = [0, 0, 0, 0]

    return render_template("adminView.html",
                           user=current_user,
                           user_list=list,
                           team_list=teams,
                           teams_data=teams_data,
                           readiness=readinessScores,
                           hours=sleepDurations,
                           quality=sleepScores,
                           nutrition=cals,
                           sleepGraphJSON=sleepGraphJSON,
                           readinessGraphJSON=readinessGraphJSON,
                           nutritionGraphJSON=nutritionGraphJSON,
                           teamGraphJSON=teamGraphJSON)


@views.route("/athleteView/<colby_email>", methods=['GET', 'POST'])
@protect_athlete_view
def athleteView(colby_email, role):
    '''Athlete dashboard view: displays daily values
    (sleep, nutrition, readiness) for a specific athlete on a specific team.'''

    athlete_role = Role.query.filter_by(name='athlete').first()

    if (role == athlete_role):
        athlete_user = current_user

    else:
        athlete_user = User.query.filter_by(email=colby_email).first()

    # READINESS GRAPH
    readinessScores = ([readiness.ReadinessScore
                        for readiness in athlete_user.readiness])

    if len(readinessScores) > 0:
        readinessScore = readinessScores[0]
        readinessV = [readinessScore, (100-readinessScore)]
    else:
        readinessV = [0]

    readinessGraphJSON = pie_chart(readinessV, 'Readiness',
                                   ['Readiness Score'])

    # NUTRITION GRAPH
    calories = ([nutrition.calories for nutrition in athlete_user.nutrition])

    if len(calories) > 0:
        calorie = calories[0]
        nutritionV = [calorie, (3000-calorie)]
    else:
        nutritionV = [0]

    nutritionGraphJSON = pie_chart(nutritionV, 'Nutrition',
                                   ['Nutrition Score'])

    # SLEEP GRAPH
    sleepDurations = ([sleep.TotalSleepDuration
                       for sleep in athlete_user.sleep])

    sleepScores = ([sleep.TotalSleepScore
                       for sleep in athlete_user.sleep])

    if len(sleepDurations) > 0:
        sleepDuration = sleepDurations[0]
        sleepV = [sleepDuration, (8-sleepDuration)]
    else:
        sleepV = [0]

    sleepGraphJSON = pie_chart(sleepV, 'Sleep', ['Sleep Score'])

    # LINE GRAPH
    timeStamp = []
    list = []
    if len(readinessScores) > 0:
        for item in readinessScores:
            list.append(item)
            timeStamp.append(readinessScores.index(item))
    else:
        timeStamp = [0]
        list = [0]

    teamGraphJSON = line_chart(timeStamp, list, 'Readiness History')

    first_name = athlete_user.first_name + " "
    last_name = athlete_user.last_name
    team_list = current_user.teams
    if current_user.role == "admin":
        team_list = Team.query.all()

    return render_template("athleteView.html",
                           user=current_user,
                           sleepGraphJSON=sleepGraphJSON,
                           readinessGraphJSON=readinessGraphJSON,
                           nutritionGraphJSON=nutritionGraphJSON,
                           teamGraphJSON=teamGraphJSON,
                           readiness=readinessScores,
                           hours=sleepDurations,
                           quality=sleepScores,
                           nutrition=calories,
                           fname=first_name,
                           lname=last_name,
                           team_list=team_list)


@views.route("/connect-google-fit", methods=["GET", "POST"])
@auth_required()
def connectFit():
    if request.method == 'POST':
        print('hi')
        # TODO once connection is implemented the test_connectFit should be updated
    return render_template("connectFit.html", user=current_user)


@views.route("/fit-oauth-callback")
@auth_required()
def fitOauthCallback():
    # TODO a html template is required to display this view
    return render_template("fitOauthCallback.html", user=current_user)


@views.route("/teamView", methods=["GET", "POST"])
def changingTeamView():
    if request.form.get("teams") is not None:
        team_name = request.form.get("teams")
        print(request.form.get("teams"))
        return teamView(team_name)


@views.route("/teamView/<team_name>", methods=["GET", "POST"])
@login_required
def teamView(team_name):
    '''Coach dashboard view: displays average values
    (sleep, nutrition, readiness) for all athletes across a specific team.'''

    if (team_name == "" and request.form.get("teams") is None):
        team_name = request.form.get("teams")

    current_team = Team.query.filter_by(name=team_name).first()

    readinessScores = []
    readinessIndexes = []
    calories = []
    sleepScores = []
    sleepDurations = []
    for index, user in enumerate(current_team.users):
        readinessScores += [r.ReadinessScore for r in
                            current_team.users[index].readiness]
        readinessIndexes += [r.RecoveryIndexScore for r in
                             current_team.users[index].readiness]
        calories += [n.calories for n in
                     current_team.users[index].nutrition]
        sleepScores += [s.TotalSleepScore for s in
                        current_team.users[index].sleep]
        sleepDurations += [s.TotalSleepDuration for s in
                           current_team.users[index].sleep]

    # READINESS GRAPH
    if len(readinessScores) > 0:
        readinessScore = round(mean(readinessScores), 1)
        readinessV = [readinessScore, (100-readinessScore)]
    else:
        readinessV = [0]

    readinessGraphJSON = pie_chart(readinessV, 'Readiness',
                                   ['Readiness Score'])

    # NUTRITION GRAPH

    if len(calories) > 0:
        calorie = round(mean(calories), 1)
        nutritionV = [calorie, (3000-calorie)]
    else:
        nutritionV = [0]

    nutritionGraphJSON = pie_chart(nutritionV, 'Nutrition', 'Nutrition Score')

    # SLEEP GRAPH

    if len(sleepDurations) > 0:
        sleepDuration = round(mean(sleepDurations), 1)
        sleepV = [sleepDuration, (8-sleepDuration)]
    else:
        sleepV = [0]

    sleepGraphJSON = pie_chart(sleepV, 'Sleep', ['Sleep Score'])

    # LINE GRAPH
    timeStamp = []
    list = []
    if len(readinessScores) > 0:
        for item in readinessScores:
            list.append(item)
            timeStamp.append(readinessScores.index(item))
    else:
        timeStamp = [0]
        list = [0]

    teamGraphJSON = line_chart(timeStamp, list, 'Readiness History')

    team_name = team_name.replace("_", " ")
    team_name = string.capwords(team_name)

    athletes = {athlete for athlete in current_team.users
                if athlete.role == 'athlete'}
    athlete_data = {}

    for athlete in athletes:
        athlete_sleep = 0
        athlete_quality = 0
        athlete_readiness = 0
        athlete_calories = 0
        athlete_notes = " "
        if len(athlete.sleep) != 0:
            for sleep in athlete.sleep:
                athlete_sleep += sleep.TotalSleepDuration
                athlete_quality += sleep.TotalSleepScore
            athlete_sleep = athlete_sleep/len(athlete.sleep)
            athlete_quality = athlete_quality/len(athlete.sleep)
        else:
            athlete_sleep = 0
            athlete_quality = 0
        if len(athlete.readiness) != 0:
            for readiness in athlete.readiness:
                athlete_readiness += readiness.ReadinessScore
            athlete_readiness = athlete_readiness/len(athlete.readiness)
        else:
            athlete_readiness = 0
        if len(athlete.nutrition) != 0:
            for nutrition in athlete.nutrition:
                athlete_calories += nutrition.calories
            athlete_calories = athlete_calories/len(athlete.nutrition)
        else:
            athlete_readiness = 0

        athlete_data[athlete.id] = [round(athlete_sleep, 1),
                                    round(athlete_quality, 1),
                                    round(athlete_readiness, 1),
                                    round(athlete_calories, 1), athlete_notes]

    team_list = current_user.teams
    if current_user.role == "admin":
        team_list = Team.query.all()
    return render_template("teamView.html", user=current_user,
                           sleepGraphJSON=sleepGraphJSON,
                           readinessGraphJSON=readinessGraphJSON,
                           nutritionGraphJSON=nutritionGraphJSON,
                           teamGraphJSON=teamGraphJSON,
                           TeamName=team_name,
                           athletes=athletes,
                           athlete_data = athlete_data,
                           readiness=readinessScores,
                           hours=sleepDurations,
                           quality=sleepScores,
                           nutrition=calories,
                           team_list = team_list
                           )


@views.route("/permissions/<chosen_user_id>", methods=['GET', 'POST'])
def changeRole(chosen_user_id):
    newRole = request.form.get("changeRole")
    print(current_user)
    print(newRole)
    chosen_user = User.query.filter_by(id=chosen_user_id).first()
    if newRole:
        if chosen_user != current_user:
            print("YES YES YES")
            chosen_user.role = newRole
            db.session.commit()
    return permissions()


@views.route("/permissions", methods=['GET', 'POST'])
@auth_required()
def permissions(): 
    id = request.form.get('users')
    if id:
        chosen_user = User.query.filter_by(id=id).first()
    else:
        chosen_user = current_user

    list = User.query.all()
    role = request.form.get('select_role')
    if role:
        select_role = role
    else:
        select_role = 'athlete'
    team_list = Team.query.all()

    return render_template("permissions.html", user=current_user,
                           user_list=list,
                           selected_role=select_role,
                           selected_user=chosen_user,
                           team_list=team_list)


@views.route("/permission", methods=['GET', 'POST'])
def adduser():

    if request.method == 'POST':

        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        role = request.form.get('roles')

        user = User.query.filter_by(email=email).first()

        if not re.match(r"([^@]{3,})(@)(colby.edu)", email):
            flash("Colby email address required")
        elif user:
            flash('Email already exists.')
        elif len(first_name) == 0 or len(last_name) == 0:
            flash('First and Lastname required')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.')
        else:
            # add user to database
            new_user = User(email=email,
                            password=generate_password_hash(password,
                                                            method='sha256'),
                            role=role,
                            first_name=first_name,
                            last_name=last_name)
            teams = request.form.getlist('teams')

            if len(teams) > 0:
                for team_name in teams:
                    print(team_name)
                    team = Team.query.filter_by(name=team_name).first()
                    team.users += [new_user]

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')

    id = request.form.get('users')
    selected_user = User.query.filter_by(id=request.form.get('users')).first() if id else current_user

    role = request.form.get('select_role')
    selected_role = role if role else "athlete"

    team_list = Team.query.all()
    list = User.query.all()

    return render_template("permissions.html",
                           user=current_user,
                           user_list=list,
                           selected_user=selected_user,
                           selected_role=selected_role,
                           team_list=team_list)


def allowed_file(filename):
    '''Helper function for upload()'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {"csv"}


@views.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    '''Upload function: parses uploaded csv file
    and inserts it into the database.'''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                   filename))

            # parse the csv file and insert it into the db
            data_type = filename.rsplit(".")[0].lower()
            parse_csv(data_type=data_type, filename=filename)
            flash('Database up to date', 'success')
    return render_template("upload.html", user=current_user)


@views.route("/remove", methods=["GET", "POST"])
@login_required
def remove_users():

    coach = Role.query.filter_by(name='coach').first()
    athlete = Role.query.filter_by(name='athlete').first()

    is_coach = User.roles.contains(coach)
    coaches = User.query.where(is_coach)

    is_athlete = User.roles.contains(athlete)
    athletes = User.query.where(is_athlete)

    return render_template('removeUsers.html',
                           user=current_user,
                           coaches=coaches,
                           athletes=athletes)


@views.route("/remove/<string:user_email>", methods=["GET", "POST"])
@login_required
def remove(user_email):
    usr = User.query.filter_by(email=user_email).first()
    db.session.delete(usr)
    db.session.commit()
    return redirect(url_for('views.remove_users'))
