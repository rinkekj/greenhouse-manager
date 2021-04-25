from flask import url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import (
    BooleanField,
    StringField,
    SubmitField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from app.models import Contact


class LoginForm(FlaskForm):
    email = EmailField('Email',
                       validators=[InputRequired(),
                                   Length(1, 64),
                                   Email()])
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    first_name = StringField('First name',
                             validators=[InputRequired(),
                                         Length(1, 64)])
    last_name = StringField('Last name',
                            validators=[InputRequired(),
                                        Length(1, 64)])
    email = EmailField('Email',
                       validators=[InputRequired(),
                                   Length(1, 64),
                                   Email()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Contact.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered. (Did you mean to '
                                  '<a href="{}">log in</a> instead?)'.format(
                                      url_for('account.login')))
