'''Backend to send emails using mailtrap api'''

from flask_mailman.backends.base import BaseEmailBackend
from requests import request
from json import dumps, loads
import os

from dotenv import load_dotenv

load_dotenv()


class EmailBackend(BaseEmailBackend):
    '''Custom Flask-Mailman backend for sending emails using Mailtrap API'''

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)

    def send_messages(self, email_messages):
        '''Send one or more EmailMessage objects and return the number of
        email messages sent.'''

        sent = 0

        if email_messages:
            for message in email_messages:
                sent += self._send(message)

        return sent

    def _send(self, message):
        '''Helper method to send one EmailMessage'''

        msg_data = {
            'from': {'email': os.environ.get('MAIL_DEFAULT_SENDER'),
                     'name': 'Colby Athlete Managment System'},
            'to': [{'email': message.to[0]}],
            'subject': message.subject,
            'text': message.body
            }

        headers = {
            "Authorization": 'Bearer ' + os.environ.get('MAIL_AUTHORIZATION'),
            "Content-Type": "application/json"
        }

        url = "https://send.api.mailtrap.io/api/send"

        response = request("POST", url, headers=headers, data=dumps(msg_data))

        response_json = loads(response.text)

        if response_json['success']:
            return 1
        else:
            return 0
