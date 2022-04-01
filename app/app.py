from flask import Flask, render_template, redirect, url_for, session, request
from forms import RegistrationForm, LoginForm
from datetime import timedelta

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
        #flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    else:
      if "user" in session:
        return redirect(url_for("posts"))
      
      return render_template('register.html', title='Register', form=form)

#login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #flash(f'Account {form.username.data} loggedin!', 'success')
        session.permanent = True
        user = request.form["nationID"]
        session["user"] = user
        return redirect(url_for('posts'))
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
