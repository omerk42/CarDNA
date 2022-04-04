from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, RadioField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


types = [('male', 'male'), ('female', 'female')]
cities = [('Riyadh','Riyadh'),('Makkah','Makkah'),('Madinah','Madinah'),('Qassim','Qassim'),('Eastern Province','Eastern Province'),('Asir','Asir'),('Tabuk','Tabuk'),('Hail','Hail'),('Northern Borders','Northern Borders'),('Jazan','Jazan'),('Najran','Najran'),('Bahah','Bahah'),('Jawf','Jawf')]
seats = [('2','2'),('5','5'),('8','8')]
marks = ['Abarth','Acura','Alfa Romeo','Aston Martin','Audi','Bentley','BMW','Buick','Cadillac','Chevrolet','Chrysler','Citroen','Dacia','Dodge','Ferrari','Fiat','Ford','GMC','Honda','Hummer','Hyundai','Infiniti','Isuzu','Jaguar','Jeep','Kia','Lamborghini','Lancia','Land Rover','Lexus','Lincoln','Lotus','Maserati','Mazda','Mercedes-Benz','Mercury','Mini','Mitsubishi','Nissan','Opel','Peugeot','Pontiac','Porsche','Ram','Renault','Saab','Saturn','Scion','Seat','Skoda','Smart','SsangYong','Subaru','Suzuki','Tesla','Toyota','Volkswagen','Volvo','Wiesmann']
plate_types = ['Private cars', 'Public transport', 'Commercial', 'Diplomatic']
car_parts = ['roof', 'engine cover', 'trunk', 'front bumper', 'rear bumper', 'right front wing', 'left front wing', 'right rear wing', 'left rear wing', 'right front door', 'left front door', 'right rear door', 'left rear door']

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegistrationForm(FlaskForm):

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
    nationID = StringField('National ID', validators=[DataRequired(),Length(10), Regexp('^[1-2][0-9]{9}$', message='Enter valid nation ID')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')

class RepairmentForm(FlaskForm):
  # Person data
  nationID = StringField('National ID', validators=[DataRequired(), Length(10), Regexp('^[1-2][0-9]{9}$', message='Enter valid nation ID')])
  fname = StringField('First name', validators=[DataRequired(), Length(min=4, max=20)])
  mname = StringField('Middle name', validators=[DataRequired(), Length(min=4, max=20)])
  lname = StringField('Last name', validators=[DataRequired(), Length(min=4, max=20)])
  gender = SelectField('Gender', choices =types, validators=[DataRequired()])
  phonenumber = StringField('Phone number', validators=[DataRequired(), Length(10), Regexp('^[0][5][0-9]{8}$', message="Phonenumber must be like 05**")])
  dob = DateField('Date of birth', validators=[DataRequired()])

  # Car data
  car_vin = StringField('Car VIN', validators=[DataRequired(), Length(17), Regexp('^[(A-H|J-N|P|R-Z|0-9)]{17}$', message="Enter a valid VIN")])
  car_seats = SelectField('Number of seats', choices=seats, validators=[DataRequired()])
  car_mark = SelectField('Mark', choices=marks, validators=[DataRequired()])
  car_model = StringField('Model (name)', validators=[DataRequired(), Length(min=4, max=20)])
  car_year = StringField('Manufacturing year', validators=[DataRequired(), Regexp('^(19|20|21|22)\d{2}$', message='enter valid year between 1900 and 2099')])
  car_color = StringField('Color', validators=[DataRequired(), Length(min=3, max=10)])
  car_plate_letters = StringField('Plate letters', validators=[DataRequired(), Length(3), Regexp('^[A-Z]{3}$', message='only capital english letters allowed')])
  car_plate_nums = StringField('Plate numbers', validators=[DataRequired(), Length(4), Regexp('^[0-9]{4}$', message='only numbers allowed')])
  car_plate_type = SelectField('Plate type', choices=plate_types, validators=[DataRequired()])
  car_since_date = StringField('Year of ownership', validators=[DataRequired(), Regexp('^(19|20|21|22)\d{2}$')])

  # Repair data
  rep_permission_paper_id = StringField('Repairment Paper ID', validators=[DataRequired(), Length(8), Regexp('^[0-9]{8}$', message='only numbers allowed')])
  rep_date = DateField('Date of repairment', validators=[DataRequired()])
  rep_car_part = MultiCheckboxField('Car parts', choices=car_parts)
  rep_desc = StringField('Repairment Decription', validators=[DataRequired(), Length(min=4, max=100)])

  submit = SubmitField('Record')


class addRepairmentForm(FlaskForm):
    car_vin = StringField('Car VIN', validators=[DataRequired(), Length(17), Regexp('^[(A-H|J-N|P|R-Z|0-9)]{17}$', message="Enter a valid VIN")])
    # Repair data
    rep_permission_paper_id = StringField('Repairment Paper ID', validators=[DataRequired(), Length(8), Regexp('^[0-9]{8}$', message='only numbers allowed')])
    rep_date = DateField('Date of repairment', validators=[DataRequired()])
    rep_car_part = MultiCheckboxField('Car parts', choices=car_parts)
    rep_desc = StringField('Repairment Decription', validators=[DataRequired(), Length(min=4, max=100)])
    submit = SubmitField('Record')