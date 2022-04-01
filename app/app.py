from flask import Flask, render_template, redirect, url_for, session, request, flash
from auth import *
from forms import RegistrationForm, LoginForm
from datetime import timedelta
from pprint import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = "cusSca2dwdhcfGbjkJhGQIaC0zPQJRtW"
app.permanent_session_lifetime = timedelta(minutes=5)

all_posts = [
    {
        'title': 'Post 1',
        'content': "post 1 content",
        'author': "Mike"
    },
    {
        'title': 'Post 2',
        'content': "post 2 content"
    }
]

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
        return redirect(url_for("posts"))
      
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
        return redirect(url_for('posts'))
      else:
        flash(f'National ID/ password is not correct!', 'danger')
        return render_template('login.html', title='Login', form=form)

    # GET request
    else:
      if "user" in session:
        return redirect(url_for("posts"))
      
      return render_template('login.html', title='Login', form=form)

# main program, filling repairment form (needes login)
@app.route('/posts')
def posts():
    if "user" in session:
      return render_template('posts.html', posts=all_posts)
    else:
      return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
