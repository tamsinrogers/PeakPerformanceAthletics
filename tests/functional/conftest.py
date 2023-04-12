import pytest
from website import create_app, db
from flask_mailman import Mail
from os import environ
from flask_login import LoginManager
from flask_security.core import _user_loader


@pytest.fixture(scope="function")
def flask_app():
    app = create_app()

    app.config['TESTING'] = True
    app.config['LOGIN_DISABLED'] = False

    app.config['SECURITY_PASSWORD_SALT'] = \
        environ.get('SECURITY_PASSWORD_SALT')
    app.config['SECURITY_POST_LOGIN_VIEW'] = '/user_redirect'
    app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER')
    app.config['MAIL_BACKEND'] = 'website.backend'

    app.config["WTF_CSRF_ENABLED"] = False
    # Our test emails/domain isn't necessarily valid
    app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}
    # Make this plaintext for most tests - reduces unit test time by 50%
    app.config["SECURITY_PASSWORD_HASH"] = "plaintext"

    login_manager = LoginManager()
    login_manager.login_view = 'security.login'
    login_manager.init_app(app)

    # set login manager to use flask-security user loader
    login_manager.user_loader(_user_loader)

    Mail(app)

    yield app


@pytest.fixture(scope="function")
def test_client(flask_app):
    yield flask_app.test_client()
    


def log_in(test_client, email, password):
    return test_client.post('/login',
                            data={'email': email,
                                  'password': password},
                            follow_redirects=True)
