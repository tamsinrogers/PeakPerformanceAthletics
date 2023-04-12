from conftest import log_in, test_client, flask_app
from website.models import User, Team
from website import db
import pandas as pd


def test_login(test_client):
    login_response = log_in(test_client, "matt@colby.edu", "1234567890")
    assert login_response.status_code == 200

    # fail a login
    login_response = log_in(test_client, "nobody@colby.edu", "00000000000")


def test_home(test_client):
    """Test redirect to login."""
    # access the home page
    response = test_client.get("/", follow_redirects=True)

    # should be redirected successfully to auth.login
    assert response.status_code == 200
    assert b"login" in response.data
    # check that it was only redirected once
    assert len(response.history) == 1
    # should redirect to the login page
    assert response.request.path == "/login"


def test_adminView(test_client):
    # log in successfully
    login_response = log_in(test_client, "anne@colby.edu", "1234567890")
    assert login_response.status_code == 200
    # access the adminView page
    response = test_client.get("/adminView")

    assert response.status_code == 200
    assert response.request.path == "/adminView"
    # no redirects
    assert len(response.history) == 0
    assert b"Sleep" in response.data
    assert b"Nutrition" in response.data
    assert b"Readiness" in response.data


def test_connectFit(test_client):
    # TODO once connection is implemented this test should be updated
    # log in successfully
    login_response = log_in(test_client, "matt@colby.edu", "1234567890")
    assert login_response.status_code == 200

    response = test_client.get("/connect-google-fit")
    assert response.status_code == 200
    assert response.request.path == "/connect-google-fit"
    assert b"Google Fit" in response.data


def test_fitOauthCallback(test_client):
    # TODO a html template is required to display this view
    pass


def test_teamView(test_client):
    # TODO Write a test for this view
    # How does the redirecting to the correct team work?
    pass


def test_changingTeamView(test_client):
    # TODO I don't really know how this view works so I will leave it for someone else
    pass


def test_changeRole(test_client):
    # TODO I don't really know how this view works so I will leave it for someone else
    pass


def test_permissions(flask_app, test_client):
    # log in successfully
    login_response = log_in(test_client, "anne@colby.edu", "1234567890")
    assert login_response.status_code == 200

    # access permissions page
    response = test_client.get("/permissions")
    assert response.status_code == 200
    assert response.request.path == "/permissions"
    assert b"Permissions" in response.data


def test_adduser(test_client):
    # log in anne
    login_response = log_in(test_client, "anne@colby.edu", "1234567890")
    assert login_response.status_code == 200
    # test adding a user with a bad email
    bad_email_data_dict = {
        "email": "someone@gmail.com",
        "first_name": "Milo",
        "last_name": "Lani-Caputo",
        "password": "1234567890",
        "role": "athlete"
    }
    no_name_data_dict = {
        "email": "someone@colby.edu",
        "first_name": "",
        "last_name": "",
        "password": "1234567890",
        "role": "athlete"
    }
    # good_data_dict = {
    #     "email": "someone@colby.edu",
    #     "first_name": "Milo",
    #     "last_name": "Lani-Caputo",
    #     "password": "1234567890",
    #     "role": "athlete"
    # }
    with test_client as client:
        bad_email_response = client.post("/permission", data=bad_email_data_dict)
        assert not User.query.filter_by(email="someone@gmail.com").first()
    with test_client as client:
        no_name_response = client.post("/permission", data=no_name_data_dict)
        assert not User.query.filter_by(email="someone@colby.edu").first()
    # with test_client as client:
    #     good_response = client.post("/permission", data=good_data_dict)
    #     assert User.query.filter_by(email="someone@colby.edu").first()
    #     # remove from db
    #     user = User.query.filter_by(email="someone@colby.edu").first()
    #     db.session.delete(user)
    #     db.session.commit()



def test_remove(test_client):
    pass


def test_athlete_view(flask_app, test_client):
    # log in matt
    login_response = log_in(test_client, "matt@colby.edu", "1234567890")
    assert login_response.status_code == 200
    # test that Matt's athlete view loads properly
    response = test_client.get('/athleteView/matt', follow_redirects=True)
    assert response.status_code == 200
    assert b"Matt" in response.data


def test_upload_view(flask_app, test_client):
    # log in matt
    login_response = log_in(test_client, "matt@colby.edu", "1234567890")
    assert login_response.status_code == 200

    # test GET
    get_response = test_client.get('/upload', follow_redirects=True)
    assert get_response.status_code == 200
    assert b"Upload Data" in get_response.data

    # test POST
    with flask_app.app_context():
        test_email = 'unregistered_user@colby.edu'
        test_word = 'athlete'
        assert User.query.filter_by(email=test_email).first() is None
        test_user_dict = {
                'email': [test_email],
                'first_name': [test_word],
                'last_name': [test_word],
                'password': [test_word],
                'role': [test_word]
              }
        test_user_df = pd.DataFrame(test_user_dict)
        test_file = "user.csv"
        test_user_df.to_csv(test_file)
        test_data = {
            'file': (open(test_file, 'rb'), test_file)
        }
        test_client.post('/upload', data=test_data)
        usr = User.query.filter_by(email=test_email).first()
        assert usr is not None
        assert usr.email == test_email
        assert usr.first_name == test_word
        assert usr.last_name == test_word
        assert usr.password == test_word
        assert usr.role == test_word
        db.session.delete(usr)
        db.session.commit()

def test_permissions(test_client):
    #test that we are on the permissions page
    response = test_client.get("/permissions", follow_redirects=True)
    assert response.status_code == 200
    assert b"permissions" in response.data
    #check that admintest's role can be changed.
    admintest = User(email = "adtest23@colby.edu", first_name = "No", last_name = "Body", password = "123456789", role = "admin")

    assert admintest.role == "admin"
    test_client.post('/permissions', data={
                    'email': ['adtest23@colby.edu'],
                    'first_name': ['No'],
                    'last_name': ['Body'],
                    'password': ['123456789'],
                    'role': ['athlete']
                })
    assert admintest.role == 'admin'
    assert admintest.role != 'athlete'


def test_team_view(test_client):
    #test that we are on the team view page
    newteam = Team(name="Soccer")
    assert newteam.name != "Men's Ultimate"
    assert newteam.name == "Soccer"
    response = test_client.get("/teamView/Soccer", follow_redirects=True)
    assert response.status_code == 200
    assert b"Soccer" in response.data



def test_admin_view(test_client):
    #test that we are on the admin page
    log_in(test_client, "anne@colby.edu", "1234567890")
    response = test_client.get("/adminView")
    assert response.status_code == 200
    assert b"Readiness" in response.data
    assert b"Sleep" in response.data
    assert b"Quality" in response.data    
    assert b"Calorie Intake" in response.data