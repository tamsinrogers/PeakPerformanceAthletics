'''THIS FILE (MODELS.PY) STORES THE CLASS DATA FOR A USER: HAWKINS (FORCE),
SLEEP, NUTRITION, READINESS'''

from . import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy.sql import func
from os.path import dirname
import pandas as pd
from datetime import datetime
from flask import flash


class Hawkins(db.Model):
    '''The Hawkins class.  Stores force data.'''

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date(), default=func.now())

    peak_force = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    '''The User class.  Stores User data and relationships
    (notes, hawkins, nutrition, sleep, readiness).'''

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    role = db.Column(db.String(150))

    # relationships down here
    notes = db.relationship('Note', backref='user')
    hawkins = db.relationship('Hawkins', backref='user')
    nutrition = db.relationship('Nutrition', backref='user')
    sleep = db.relationship('Sleep', backref='user')
    readiness = db.relationship('Readiness', backref='user')
    # teams = db.relationship('Team')

    # Columns added for flask_security compatability:
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=True)

    # Currently have redundant columns 'role' and 'roles.' When flask_security
    # integration is complete 'roles' will replace 'role'
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):

    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    permissions = db.Column(db.UnicodeText(), nullable=True)


class UserRoles(db.Model):

    __tablename__ = 'user_roles'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


users_table = db.Table('users',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('user.id'), primary_key=True),
                       db.Column('team_id', db.Integer,
                                 db.ForeignKey('team.id'), primary_key=True))


class Team(db.Model):
    '''The Team class.  Stores data for users in a team.'''

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    users = db.relationship('User', secondary=users_table, lazy='subquery',
                            backref=db.backref('teams', lazy=True))


class Note(db.Model):
    '''The Notes class.  Stores sports medicine note data.'''
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Nutrition(db.Model):
    '''The Nutrition class.  Stores nutrition data.
    FOCUS VARIABLE: CALORIES'''

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date(), default=func.now())
    calories = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Sleep(db.Model):
    '''The Sleep class.  Stores sleep data.
    FOCUS VARIABLE: TOTALSLEEPDURATION'''

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date(), default=func.now())

    TotalSleepScore = db.Column(db.Integer)
    TotalSleepDuration = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Readiness(db.Model):
    '''The Readiness class.  Stores readiness data.
    FOCUS VARIABLE: READINESSSCORE'''

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date(), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    RecoveryIndexScore = db.Column(db.Integer)  # From Jonna's csv files
    ReadinessScore = db.Column(db.Integer)  # From Jonna's csv files

def add_and_commit_to_db(data):
    db.session.add(data)
    db.session.commit()


def parse_csv(data_type: str, filename: str) -> None:
    '''Parses a given csv file and adds user data from that file to the
    database.'''
    # get the csv directory and merge it with filename
    csv_directory = f"{dirname(dirname(__file__))}/csvs"
    filepath = f"{csv_directory}/{filename}"
    # read the data from the csv
    csv_data = pd.read_csv(filepath_or_buffer=filepath, header=0)

    # conditional data ingestion
    if data_type == "user":
        for row in csv_data.itertuples():
            try:
                if not User.query.filter_by(email=row.email).first():
                    # create a new User object
                    user = User(
                        email=row.email,
                        first_name=row.first_name,
                        last_name=row.last_name,
                        password=row.password,
                        role=row.role
                    )
                    # add the user to the database
                    add_and_commit_to_db(user)
            except Exception:
                flash(f"Faulty entry in {filename} on row {row.Index + 1},\
                      not included in update", 'danger')

    elif data_type == "nutrition":
        for row in csv_data.itertuples():
            try:
                # create a new Nutrition object
                nutrition = Nutrition(
                    date=datetime.strptime(row.date, '%m/%d/%Y'),
                    calories=row.calories,
                    user=User.query.filter_by(email=row.email).first()
                )
                # add the nutrition object to the database
                add_and_commit_to_db(nutrition)
            except Exception:
                flash(f"Faulty entry in {filename} on row {row.Index + 1},\
                      not included in update", 'danger')

    elif data_type == "readiness":
        for row in csv_data.itertuples():
            try:
                # create a new Readiness object
                readiness = Readiness(
                    date=datetime.strptime(row.date, '%m/%d/%Y'),
                    RecoveryIndexScore=row.recovery_index_score,
                    ReadinessScore=row.readiness_score,
                    user=User.query.filter_by(email=row.email).first()
                )
                # add the readiness object to the database
                add_and_commit_to_db(readiness)
            except Exception:
                flash(f"Faulty entry in {filename} on row {row.Index + 1},\
                      not included in update", 'danger')

    elif data_type == "hawkins":
        for row in csv_data.itertuples():
            # create a new Readiness object
            hawkins = Hawkins(
                date=datetime.strptime(row.date, '%m/%d/%Y'),
                peak_force=row.at["peak_force"],
                user=User.query.filter_by(email=row.email).first()
            )
            # add the readiness object to the database
            add_and_commit_to_db(hawkins)
    # else, sleep data
    elif data_type == "sleep":
        for row in csv_data.itertuples():
            try:
                # create a new Sleep object
                sleep = Sleep(
                    date=datetime.strptime(row.date, '%m/%d/%Y'),
                    TotalSleepScore=row.total_sleep_score,
                    TotalSleepDuration=row.total_sleep_duration,
                    user=User.query.filter_by(email=row.email).first()
                )
                # add the Sleep object to the database
                add_and_commit_to_db(sleep)
            except Exception:
                flash(f"Faulty entry in {filename} on row {row.Index + 1},\
                      not included in update", 'danger')

    else:
        flash(f"Error in {filename} csv format", 'danger')
