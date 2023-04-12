# Security
This app uses the [Flask-Security](https://flask-security-too.readthedocs.io/en/stable/index.html) extension to provide
- Login/logout
- Account registration and confirmation
- Password reset
- User roles

Flask-Security replaces the login and sign up views in auth.py. Default Flask-Security templates are overridden by placing custom html in `website/templates/security` the file name must match the default template name.

## Configuring App Environment
config.py performs app configuration

A .env file with the following variables is required in the top level directory to configure the app

    ## APP SECURITY ##
    SECRET_KEY='secret-key-goes-here'
    SECURITY_PASSWORD_SALT = **************************************

    ## MAIL SERVER SETTINGS ##
    MAIL_AUTHORIZATION='Bearer ********************************'
    MAIL_DEFAULT_SENDER='email@example.com'
    MAIL_TEST_ADDRESS='test@example.com'

To generate a strong `SECURITY_PASSWORD_SALT`:

    $ python3
    >>> import secrets
    >>> secrets.SystemRandom().getrandbits(128)
    **************************************

