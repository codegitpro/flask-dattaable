# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, DecimalField

from wtforms.validators import InputRequired, Email, DataRequired

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired()])
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])


class ContractForm(FlaskForm):
    username = TextField('Username'     , id='username_insert' , validators=[DataRequired()])
    contract_title = TextField('Enter email' , id='contract_insert' , validators=[DataRequired(), Email()])
    discord = TextField('Enter email'     , id='discord_insert' , validators=[DataRequired(), Email()])
    refund = TextField('Enter email'     , id='refund_insert' , validators=[DataRequired()])
    traders_address = TextField('Password'     , id='password_insert' , validators=[DataRequired()])
    payment_options = SelectField('payment_options', 
    choices = [('Bitcoin', 'Bitcoin'), ('Ethereum', 'Ethereum')])
    payment_amount = DecimalField(places=2, id='amount', validators=[DataRequired()])
    details =  TextField('Enter details', id='details_insert' , validators=[DataRequired()])