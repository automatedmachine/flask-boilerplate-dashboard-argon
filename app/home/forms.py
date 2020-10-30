# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from app import db
from app.home.models import Clients
from flask_wtf import FlaskForm
from wtforms import TextField, HiddenField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired, NumberRange
from wtforms.fields.html5 import DateField, DecimalField, EmailField, TelField

## login and registration

class ClientForm(FlaskForm):
    first_name = TextField ('First Name', id='first_name', validators=[DataRequired()])
    last_name = TextField ('Last Name', id='last_name', validators=[DataRequired()])
    email = EmailField ('Email', id='email', validators=[Email()])
    telephone = TelField ('Telephone', id='telephone')
    client_type = SelectField ('Type', id='client_type', choices=[('Adult Client'),('Child & Parent(s)'),('Multi Child Family'),('Friends'),('Experiment')])
    pro_bono = SelectField ('Pro Bono', id='pro_bono', choices=[('No'), ('Yes')])
    id = HiddenField ('Row ID', id='row_id')
    user_id = HiddenField ('User ID', id='user_id')
    

class SessionForm(FlaskForm):
    date = DateField ('Date', id='date', validators=[DataRequired()])
    client_id = SelectField ('Client', id='client_id', choices=[], validators=[DataRequired()])
    duration = DecimalField ('Duration', id='amount', places=2, validators=[DataRequired()])
    id = HiddenField ('Row ID', id='row_id')
    user_id = HiddenField ('User ID', id='user_id')
