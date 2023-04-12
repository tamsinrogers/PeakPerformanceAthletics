'''CREATES THE APP & POPULATES THE DATABASE WITH SOME INITIAL DATA'''


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, environ

from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.core import _user_loader
from flask_security.utils import hash_password
from flask_security.confirmable import confirm_user

from .forms import NameRegisterForm

import datetime
import random

from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

from .models import User, Role, Team, Hawkins, Sleep, Nutrition, Readiness

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

DB_NAME = "database.db"
# the location of the csv upload folder
UPLOAD_FOLDER = "./csvs"


def create_app() -> Flask:
    '''Creates the Flask app, imports necessary classes, tests references to
    different types of data.'''

    app = Flask(__name__)

    # Database configuration
    # terrible but I don't have admin on github so I can't add secrets
    # need this to pass tests
    if environ.get('DATABASE_URL') is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'

    else:
        uri = environ.get('DATABASE_URL')
        if uri and uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = uri

    # Security configuration
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SECURITY_PASSWORD_SALT'] = \
        environ.get('SECURITY_PASSWORD_SALT')

    # Enable registration, email confirmation and account recovery
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_CONFIRMABLE'] = True
    app.config['SECURITY_RECOVERABLE'] = True

    # Login configuration
    app.config['SECURITY_POST_LOGIN_VIEW'] = '/user_redirect'

    # Mail configuration
    app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER')
    app.config['MAIL_BACKEND'] = 'website.backend'

    # configure an upload folder for csv uploads
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # app.register_blueprint(auth, url_prefix='/')

    # similar bad fix as above to pass test
    if environ.get('DATABASE_URL') is None:

        # only create database on github
        create_database(app)

    # create flask-security
    app.security = Security(app, user_datastore,
                            confirm_register_form=NameRegisterForm)

    populate(app, user_datastore)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # set login manager to use flask-security user loader
    login_manager.user_loader(_user_loader)

    return app


def create_database(app: Flask):
    '''Creates a database if one does not already exist within the directory'''

    if not path.exists('instance/' + DB_NAME):
        print('Created Database!')

        # use app context in order to initialize properly
        with app.app_context():
            db.create_all()


def populate(app: Flask, ds: SQLAlchemyUserDatastore):
    '''Creates some users and defines relationships with their data.'''

    with app.app_context():

        # try to get admin from user datastore
        user = ds.find_user(email='anne@colby.edu')

        # if admin exists do nothing
        if user:
            pass

        # otherwise create roles and admin
        else:

            # create roles
            admin = ds.create_role(name='admin',
                                   description='administrator account')
            coach = ds.create_role(name='coach',
                                   description='coach account')
            athlete = ds.create_role(name='athlete',
                                     description='athlete account')

            matt = ds.create_user(email="matt@colby.edu",
                                  first_name="Matt",
                                  last_name="Cerrato",
                                  role="athlete",
                                  password=hash_password("1234567890"))
            ds.add_role_to_user(matt, athlete)
            confirm_user(matt)

            milo = ds.create_user(email="milo@colby.edu",
                                  first_name="Milo",
                                  last_name="Lani-Caputo",
                                  role="athlete",
                                  password=hash_password("1234567890"))
            ds.add_role_to_user(milo, athlete)
            confirm_user(milo)

            hannah = ds.create_user(email="hannah@colby.edu",
                                    first_name="Hannah",
                                    last_name="Soria",
                                    role="coach",
                                    password=hash_password("1234567890"))
            ds.add_role_to_user(hannah, coach)
            confirm_user(hannah)

            nicole = ds.create_user(email="nicole@colby.edu",
                                    first_name="Nicole",
                                    last_name="Matamoros",
                                    role="coach",
                                    password=hash_password("1234567890"))
            ds.add_role_to_user(nicole, coach)
            confirm_user(nicole)

            anne = ds.create_user(email="anne@colby.edu",
                                  first_name="Anne",
                                  last_name="Doctor",
                                  role="admin",
                                  password=hash_password("1234567890"))
            ds.add_role_to_user(anne, admin)
            confirm_user(anne)

            ds.commit()

            # Teams
            swim = Team(name="mens_swim")
            swim.users += [matt, milo, hannah, nicole]

            tennis = Team(name="womens_tennis")
            tennis.users += [matt, milo, hannah, nicole]

            athletes = [matt, milo]
            random.seed(10)

            for athlete in athletes:
                for i in range(1, 31, 1):
                    hawkinsData = Hawkins(
                        date=datetime.date(2022, 10, i),
                        peak_force=random.randint(50, 100),
                        user_id=athlete.id
                    )
                    sleepData = Sleep(
                        date=datetime.date(2022, 10, i),
                        TotalSleepScore=random.randint(50, 100),
                        TotalSleepDuration=random.randint(0, 8),
                        user_id=athlete.id
                    )
                    nutritionData = Nutrition(
                        date=datetime.date(2022, 10, i),
                        calories=random.randint(500, 3000),
                        user_id=athlete.id
                    )
                    readinessData = Readiness(
                        date=datetime.date(2022, 10, i),
                        RecoveryIndexScore=random.randint(0, 100),
                        ReadinessScore=random.randint(1, 100),
                        user_id=athlete.id
                    )
                    athlete.hawkins.append(hawkinsData)
                    athlete.sleep.append(sleepData)
                    athlete.nutrition.append(nutritionData)
                    athlete.readiness.append(readinessData)

            db.session.add_all([matt, milo, hannah, nicole,
                                swim, tennis, anne])
            db.session.commit()
