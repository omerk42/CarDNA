from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, AnyOf


class RegistrationForm(FlaskForm):
    types = [('male', 'male'), ('female', 'female')]
    cities = [('Riyadh','Riyadh'),('Makkah','Makkah'),('Madinah','Madinah'),('Qassim','Qassim'),('Eastern Province','Eastern Province'),('Asir','Asir'),('Tabuk','Tabuk'),('Hail','Hail'),('Northern Borders','Northern Borders'),('Jazan','Jazan'),('Najran','Najran'),('Bahah','Bahah'),('Jawf','Jawf')]

    fname = StringField('First name', validators=[DataRequired(), Length(min=4, max=20)])
    mname = StringField('Middle name', validators=[DataRequired(), Length(min=4, max=20)])
    lname = StringField('Last name', validators=[DataRequired(), Length(min=4, max=20)])
    gender = SelectField('Gender', choices =types, validators=[DataRequired()])
    city = SelectField('City', choices =cities, validators=[DataRequired()])
    location = StringField('Location description', validators=[Length(max=100)])
    nationID = StringField('National ID', validators=[DataRequired(), Length(10), Regexp('^[1-2][0-9]{9}$', message='Enter valid nation ID')]) 
    phonenumber = StringField('Phone number', validators=[DataRequired(), Length(10), Regexp('^[0][5][0-9]{8}$', message="Phonenumber must be like 05**")])
    dob = DateField('Date of birth', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    comm_act_num = StringField('Commercial activity license number', validators=[DataRequired(),Length(10), Regexp('^[1-2][0-9]{9}$', message='Enter valid Commercial activity license number')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    nationID = StringField('Nation ID', validators=[DataRequired(),Length(10), Regexp('^[1-2][0-9]{9}$', message='Enter valid nation ID')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')
