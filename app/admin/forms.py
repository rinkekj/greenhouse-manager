from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    IntegerField,
    SelectField,
)

from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
    NumberRange,
    Optional,
)

from app import db, dprint
from app.models import Role, Employee, Contact

import phonenumbers
from itertools import compress


class ChangeAccountTypeForm(FlaskForm):
    role = QuerySelectField(
        'New account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    submit = SubmitField('Update role')


class NewEmployeeForm(FlaskForm):
    role = QuerySelectField('Account type', validators=[InputRequired()], get_label='name', query_factory=lambda: db.session.query(Role).order_by('permissions'))
    first_name = StringField('First name', validators=[InputRequired(), Length(1, 64)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(1, 64)])
    email = EmailField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[ InputRequired(), EqualTo('password2', 'Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    submit = SubmitField('Create')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

class ContactForm(FlaskForm):
    first_name = StringField('First name',
                validators=[InputRequired(), Length(1, 64)])
    last_name = StringField('Last name',
                validators=[InputRequired(), Length(1, 64)])
    email = EmailField('Email',
                validators=[InputRequired(), Length(1, 64), Email()])
    phone = StringField('Phone number', 
                validators=[InputRequired()])

    def validate_email(self, field):
        if Contact.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_phone(self, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            phoneNum = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

        if Contact.query.filter_by(phone=field.data).first():
            raise ValidationError('Phone number already registered.')


class SupplierForm(ContactForm):
    statesList = ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL',
                  'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
                  'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
                  'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
                  'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI',
                  'WY')
    states = list(zip(statesList, statesList))
    companyName = StringField(u'Company name',
                validators=[InputRequired(), Length(1, 64)])
    address = StringField(u'Address',
                validators=[InputRequired(), Length(1, 64)])
    city = StringField(u'City', validators=[InputRequired(), Length(1, 64)])
    zip = IntegerField(u'Zip code',
                validators=[
                    InputRequired(),
                    NumberRange(min=10000, max=99999, message='Not a valid zip code')])
    state = SelectField(u'State', choices=states, coerce=str)
    addEdit = SelectField(u'Entry', id='add_edit', coerce=int, 
                validators=[ Optional(), ])
    submit = SubmitField('Add')
