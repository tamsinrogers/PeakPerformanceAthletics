from flask_security import ConfirmRegisterForm
from wtforms.validators import DataRequired
from wtforms import StringField


class NameRegisterForm(ConfirmRegisterForm):
    first_name = StringField('First name', [DataRequired()])
    last_name = StringField('Last name', [DataRequired()])
