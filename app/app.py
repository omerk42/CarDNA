from turtle import title
from flask import Flask, render_template, redirect, url_for, session, request, flash
from auth import *
from repairForm import *
from forms import RegistrationForm, LoginForm, RepairmentForm, addRepairmentForm
from datetime import timedelta
from pprint import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = "cusSca2dwdhcfGbjkJhGQIaC0zPQJRtW"
app.permanent_session_lifetime = timedelta(minutes=10)


# landing page, POST request with VIN will be added.
@app.route('/')
def index(methods=['GET']):
    return render_template('index.html')

# register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        error = False
        if (registered_nationID(form.nationID.data)):
          flash(f'National ID {form.nationID.data} is used!', 'danger')
          error=True
        if (registered_email(form.email.data)):
          flash(f'Email {form.email.data} is used!', 'danger')
          error=True
        if (registered_phonenumber(form.phonenumber.data)):
          flash(f'Phonenumber {form.phonenumber.data} is used!', 'danger')
          error=True
        if (registered_comm_act_num(form.comm_act_num.data)):
          flash(f'Commercial activity license number {form.comm_act_num.data} is used!', 'danger')
          error=True
        if error:
          return render_template('register.html', title='Register', form=form)
        else:
          if (insert_new_user(form.data)):
            flash(f'Account created for {form.fname.data}!', 'success')
            return redirect(url_for('login'))
          else: 
            flash(f'Account not created!', 'danger')
            return redirect(url_for('register'))
    else:
      if "user" in session:
        return redirect(url_for("repairment"))
      
      return render_template('register.html', title='Register', form=form)

#login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # post request
    if form.validate_on_submit():
      if check_login(form.nationID.data, form.password.data):
        fname = get_fname_by_per_nation_id(form.nationID.data)
        flash(f'Welcome {fname}!', 'success')
        session.permanent = True
        user = request.form["nationID"]
        session["user"] = user
        return redirect(url_for('repairment'))
      else:
        flash(f'National ID/ password is not correct!', 'danger')
        return render_template('login.html', title='Login', form=form)

    # GET request
    else:
      if "user" in session:
        return redirect(url_for("repairment"))
      
      return render_template('login.html', title='Login', form=form)

# main program, filling repairment form (needes login)
@app.route('/repairment', methods=['GET', 'POST'])
def repairment():
    if "user" in session:
      form = RepairmentForm()
      if form.validate_on_submit():
        error = False
        if (registered_nationID(form.nationID.data)):
          flash(f'National ID {form.nationID.data} is regestered, use Add Repairment page!', 'danger')
          error=True
        if (registered_phonenumber(form.phonenumber.data)):
          flash(f'Phonenumber {form.phonenumber.data} is regestered, use Add Repairment page!', 'danger')
          error=True
        if (registered_car_vin(form.car_vin.data)):
          flash(f'Car VIN {form.car_vin.data} is regestered, use Add Repairment page!', 'danger')
          error=True
        if registered_rep_permission_paper_id(form.rep_permission_paper_id.data):
          flash(f'Repairment paper ID {form.rep_permission_paper_id.data} is regestered!', 'danger')
          error=True
        if not form.rep_car_part.data:
          flash(f'Car parts field is empty!', 'danger')
          error=True
        if car_since_date_bigger_current(form.car_since_date.data):
          flash(f'Year of ownership cannot be newer than current year!', 'danger')
          error=True
        if car_since_date_older_car_year(form.car_since_date.data, form.car_year.data):
          flash(f'Year of ownership cannot be older than manufacturing year!', 'danger')
          error=True
        if car_year_bigger_current(form.car_year.data):
          flash(f'Manufacturing year cannot be newer than current year!', 'danger')
          error=True
        if dob_bigger_current(form.dob.data):
          flash(f'Date of birth year cannot be newer than current year!', 'danger')
          error=True
        if rep_date_bigger_current(form.rep_date.data):
          flash(f'Repairment year must be in current year!', 'danger')
          error=True
        if rep_date_older_car_since_date(form.rep_date.data, form.car_since_date.data):
          flash(f'Repairment year cannot be older than year of ownership!', 'danger')
          error=True
        
        if error:
          return render_template('repairment.html', form=form, title="Repairment")
        else:
          if insert_new_form(form.data):
            flash('Repairment added successfully!', 'success')
            return redirect(url_for('index'))
          else:
            flash('Error occured!', 'danger')
            return render_template('repairment.html', form=form, title="Repairment")
        
      return render_template('repairment.html', form=form, title="Repairment")
    else:
      flash('You have to login first', 'info')
      return redirect(url_for("login"))

# main program, filling repairment form (needes login)
@app.route('/addRepairment', methods=['GET', 'POST'])
def addRepairment():
  if "user" in session:
    form = addRepairmentForm()
    if form.validate_on_submit():
        error = False
        if (not registered_car_vin(form.car_vin.data)):
          flash(f'Car VIN {form.car_vin.data} is not regestered, use New Repairment page!', 'danger')
          error=True
        elif rep_date_older_car_since_date(form.rep_date.data, get_car_since_date_by_car_vin(form.car_vin.data)):
          flash(f'Repairment year cannot be older than year of ownership!', 'danger')
          error=True
        if registered_rep_permission_paper_id(form.rep_permission_paper_id.data):
          flash(f'Repairment paper ID {form.rep_permission_paper_id.data} is regestered!', 'danger')
          error=True
        if not form.rep_car_part.data:
          flash(f'Car parts field is empty!', 'danger')
          error=True
        if rep_date_bigger_current(form.rep_date.data):
          flash(f'Repairment year must be in current year!', 'danger')
          error=True
        

        if error:
          return render_template("addRepairment.html", form=form, title="Repairment")
        else:
          if pre_insert_new_repairement(form.data):
            flash('Repairment added successfully!', 'success')
            return redirect(url_for('index'))
          else:
            flash('Error occured!', 'danger')
            return render_template('addRepairment.html', form=form, title="Repairment")

    return render_template("addRepairment.html", form=form, title="Repairment")
  else:
    flash('You have to login first', 'info')
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
