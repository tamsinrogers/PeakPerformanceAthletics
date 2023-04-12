from website.backend import EmailBackend
from flask_mailman import EmailMessage
import os

from conftest import flask_app

from dotenv import load_dotenv

load_dotenv()


def test_send_emails(flask_app):
    '''tests the send_emails() function of MailtrapBackend'''

    with flask_app.app_context():
        test_message = EmailMessage(subject='Test',
                                    body='This email was sent in the process '
                                         + 'of testing the Colby Athlete '
                                         + 'Managment System email backend.',
                                    to=[os.environ.get('MAIL_TEST_ADDRESS')])

        test_backend = EmailBackend()

        n_sent = test_backend.send_messages([test_message])

        assert n_sent > 0
