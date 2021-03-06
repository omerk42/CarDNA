from flask import Flask, render_template, redirect, url_for, session, request, flash
from auth import *
from repairForm import *
from car_info import *
from forms import RegistrationForm, LoginForm, RepairmentForm, addRepairmentForm
from datetime import timedelta
from pprint import pprint
from markupsafe import escape


app = Flask(__name__, static_url_path='/static')
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
          flash(f'National ID {form.nationID.data} is used!', 'red')
          error=True
        if (registered_email(form.email.data)):
          flash(f'Email {form.email.data} is used!', 'red')
          error=True
        if (registered_phonenumber(form.phonenumber.data)):
          flash(f'Phonenumber {form.phonenumber.data} is used!', 'red')
          error=True
        if (registered_comm_act_num(form.comm_act_num.data)):
          flash(f'Commercial activity license number {form.comm_act_num.data} is used!', 'red')
          error=True
        if error:
          return render_template('register.html', form=form)
        else:
          if (insert_new_user(form.data)):
            flash(f'Account created for {form.fname.data}!', 'green')
            return redirect(url_for('login'))
          else: 
            flash(f'Account not created!', 'red')
            return redirect(url_for('register'))
    else:
      if "user" in session:
        return redirect(url_for("options"))
      
      return render_template('register.html', form=form)

#login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # post request
    if form.validate_on_submit():
      if check_login(form.nationID.data, form.password.data):
        fname = get_fname_by_per_nation_id(form.nationID.data)
        flash(f'Welcome {fname}!', 'green')
        session.permanent = True
        user = request.form["nationID"]
        session["user"] = user
        return redirect(url_for('options'))
      else:
        flash(f'National ID/ password is not correct!', 'red')
        return render_template('login.html', form=form)

    # GET request
    else:
      if "user" in session:
        return redirect(url_for("options"))
      
      return render_template('login.html', form=form)

@app.route("/options", methods=["GET"])
def options():
  if "user" in session:
    return render_template('options.html')
  else:
    flash('You have to login first', 'blue')
    return redirect(url_for("login"))

@app.route("/logout", methods=['GET'])
def logout():
  del session["user"]
  return redirect(url_for('index'))

# main program, filling repairment form (needes login)
@app.route('/repairment', methods=['GET', 'POST'])
def repairment():
    if "user" in session:
      form = RepairmentForm()
      if form.validate_on_submit():
        error = False
        if (registered_nationID(form.nationID.data)):
          flash(f'National ID {form.nationID.data} is regestered, use Registered car page!', 'red')
          error=True
        if (registered_phonenumber(form.phonenumber.data)):
          flash(f'Phonenumber {form.phonenumber.data} is regestered, use Registered car page!', 'red')
          error=True
        if (registered_car_vin(form.car_vin.data)):
          flash(f'Car VIN {form.car_vin.data} is regestered, use Registered car page!', 'red')
          error=True
        if registered_rep_permission_paper_id(form.rep_permission_paper_id.data):
          flash(f'Repairment paper ID {form.rep_permission_paper_id.data} is regestered!', 'red')
          error=True
        if not form.rep_car_part.data:
          flash(f'Car parts field is empty!', 'red')
          error=True
        if car_since_date_bigger_current(form.car_since_date.data):
          flash(f'Year of ownership cannot be newer than current year!', 'red')
          error=True
        if car_since_date_older_car_year(form.car_since_date.data, form.car_year.data):
          flash(f'Year of ownership cannot be older than manufacturing year!', 'red')
          error=True
        if car_year_bigger_current(form.car_year.data):
          flash(f'Manufacturing year cannot be newer than current year!', 'red')
          error=True
        if dob_bigger_current(form.dob.data):
          flash(f'Date of birth year cannot be newer than current year!', 'red')
          error=True
        if rep_date_bigger_current(form.rep_date.data):
          flash(f'Repairment year must be in current year!', 'red')
          error=True
        if rep_date_older_car_since_date(form.rep_date.data, form.car_since_date.data):
          flash(f'Repairment year cannot be older than year of ownership!', 'red')
          error=True
        
        if error:
          return render_template('repairment.html', form=form)
        else:
          if insert_new_form(form.data):
            flash('Repairment added successfully!', 'green')
            return redirect(url_for('repairment'))
          else:
            flash('Error occured!', 'red')
            return render_template('repairment.html', form=form)
        
      return render_template('repairment.html', form=form)
    else:
      flash('You have to login first', 'blue')
      return redirect(url_for("login"))

# main program, filling repairment form (needes login)
@app.route('/addRepairment', methods=['GET', 'POST'])
def addRepairment():
  if "user" in session:
    form = addRepairmentForm()
    if form.validate_on_submit():
        error = False
        if (not registered_car_vin(form.car_vin.data)):
          flash(f'Car VIN {form.car_vin.data} is not regestered, use Registered car page!', 'red')
          error=True
        elif rep_date_older_car_since_date(form.rep_date.data, get_car_since_date_by_car_vin(form.car_vin.data)):
          flash(f'Repairment year cannot be older than year of ownership!', 'red')
          error=True
        if registered_rep_permission_paper_id(form.rep_permission_paper_id.data):
          flash(f'Repairment paper ID {form.rep_permission_paper_id.data} is regestered!', 'red')
          error=True
        if not form.rep_car_part.data:
          flash(f'Car parts field is empty!', 'red')
          error=True
        if rep_date_bigger_current(form.rep_date.data):
          flash(f'Repairment year must be in current year!', 'red')
          error=True
        

        if error:
          return render_template("addRepairment.html", form=form)
        else:
          if pre_insert_new_repairement(form.data):
            flash('Repairment added successfully!', 'green')
            return redirect(url_for('index'))
          else:
            flash('Error occured!', 'red')
            return render_template('addRepairment.html', form=form)

    return render_template("addRepairment.html", form=form)
  else:
    flash('You have to login first', 'blue')
    return redirect(url_for("login"))

@app.route("/car_info", methods=["GET"])
def show_car_info():
  car_vin = request.args.get('car_vin')
  if car_vin is not None:
    car_id = get_car_id_by_car_vin(escape(car_vin))
    if car_id:
      car, repairments, rep_ids, car_parts = get_car_repairments(car_id)
      current_date = datetime.today().strftime('%d/%m/%Y')
      repairments_num = len(repairments)
      return render_template("car_info.html", car_vin=car_vin, car=car, repairments=repairments, rep_ids=rep_ids, car_parts=car_parts, current_date=current_date, repairments_num=repairments_num)
    else:
      flash("No information for this car VIN", 'blue')
  else:
    flash("car_vin parameter should be used", 'blue')

  return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
