'''THIS FILE (AUTH.PY) HANDLES LOGIN/LOGOUT & PERMISSIONS FUNCTIONALITY'''

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Role
from werkzeug.security import generate_password_hash
from . import db, user_datastore
from flask_login import login_user, login_required, current_user
import re

auth = Blueprint('auth', __name__)


@auth.route("/user_redirect")
@login_required
def user_redirect():

    admin = Role.query.filter_by(name='admin').first()
    coach = Role.query.filter_by(name='coach').first()
    athlete = Role.query.filter_by(name='athlete').first()
    print(current_user.roles)

    if len(current_user.roles) == 0:
        user_datastore.add_role_to_user(current_user, athlete)
        user_datastore.commit()

    if current_user.roles[0] == admin:
        return redirect(url_for('views.adminView'))

    elif current_user.roles[0] == coach:
        teams = current_user.teams
        teamName = teams[0].name
        return redirect(url_for('views.teamView', team_name=teamName))

    elif current_user.roles[0] == athlete:
        colby_email = current_user.email.split('@')[0]
        return redirect(url_for('views.athleteView', colby_email=colby_email))


@auth.route('/permissions', methods=['GET', 'POST'])
def permissions():
    '''Handles various login/signup error cases and assigns permissions based
    on the user's role (admin, coach, athlete).'''
    list = User.query.all()
    if request.method == 'POST':

        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        role = request.form.get('roles')

        emailList = email.split('@')

        user = User.query.filter_by(email=email).first()
        print(email)
        if not re.match(r"([^@]{3,})(@)(colby.edu)", email):
            flash("Colby email address required")
        elif user:
            flash('Email already exists.')
        elif len(first_name) == 0:
            flash('First name required')
        elif len(last_name) == 0:
            flash('Last name required')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.')
        else:
            print("Happened")

            # add user to database
            new_user = User(email=email,
                            password=generate_password_hash(password,
                                                            method='sha256'),
                            role=role,
                            first_name=first_name,
                            last_name=last_name)

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')

    id = request.form.get('users')
    if id:
        selected_user = User.query.filter_by(
                        id=request.form.get('users')).first()
    else:
        selected_user = current_user

    role = request.form.get('select_role')
    if role:
        selected_role = role
    else:
        selected_role = 'athelte'

    return render_template("permissions.html",
                           user_list=list,
                           selected_user=selected_user,
                           selected_role=selected_role)
