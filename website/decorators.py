from functools import wraps
from flask import redirect, url_for
from flask_security import current_user
from .models import User, Role


def protect_athlete_view(f):
    '''only allows athlete page to be viewed by the athlete, their coach,
    and admin'''
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # get email from url
        email = kwargs['colby_email'] + '@colby.edu'

        # query for athlete based on email
        athlete_query = User.query.filter_by(email=email)

        # single match
        if athlete_query.count() == 1:
            athlete = athlete_query.first()

        else:
            print('oh no!')

        admin_role = Role.query.filter_by(name='admin').first()
        coach_role = Role.query.filter_by(name='coach').first()
        athlete_role = Role.query.filter_by(name='athlete').first()

        if current_user.has_role(athlete_role):

            if current_user == athlete:
                return f(*args, **kwargs, role=athlete_role)

            else:  # redirect athlete to their own athleteView
                colby_email = current_user.email.split('@')[0]
                return redirect('/athleteView/' + colby_email)

        elif current_user.has_role(coach_role):

            coach_teams = current_user.teams
            athlete_teams = athlete.teams

            athlete_on_coach_team = any(t in coach_teams for
                                        t in athlete_teams)

            if athlete_on_coach_team:
                return f(*args, **kwargs, role=coach_role)

            else:  # redirect to default coach view
                return redirect(url_for('views.teamView'))

        elif current_user.has_role(admin_role):

            # admin can see all athletes
            return f(*args, **kwargs, role=admin_role)

        else:  # user has no role
            # haven't decided how to handle this
            pass

    return decorated_function
