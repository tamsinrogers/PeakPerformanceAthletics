# Email API
To send account confirmation and password reset emails, Flask-Security uses [Flask-Mailman](https://waynerv.github.io/flask-mailman/). Flask-Mailman has an SMTP backend, but it wasn't working with [mailtrap](https://mailtrap.io/). To fix this, `backend.py` implements a custom email backend for Flask-Mailman that uses the mailtrap api to send emails instead of SMTP.

The `EmailBackend` inherits from the Flask-Mailman `BaseEmailBackend`. It overrides the `send_messages()` function and uses the helper function `_send()` to send `EmailMessage` objects using the mailtrap API.

`_send()` POSTs email messages to https://send.api.mailtrap.io/api/send as JSON data

    msg_data = {
                'from': {'email': os.environ.get('MAIL_DEFAULT_SENDER'),
                        'name': 'Colby Athlete Managment System'},
                'to': [{'email': message.to[0]}],
                'subject': message.subject,
                'text': message.body
                }

The mailtrap API uses a token in the POST request header

    headers = {
        'Authorization': 'Bearer ' + os.environ.get('MAIL_AUTHORIZATION'),
        'Content-Type': 'application/json'
    }

The custom backend is somewhat limited. It does not implement the `open()` or `close()` methods for persistent connections. It also cannot currently send an email to more than one recipient. It would not be difficult to add this functionality but it is unneccessary for just sending account confirmation and password reset emails.