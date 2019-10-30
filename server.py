"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=["POST", "GET"])
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register', methods=["GET"])
def register_form():
    """Show user registration form"""

    return render_template("registration.html")

@app.route('/register', methods=["POST"])
def register_process():
    """Handles submission of the login form"""

    # query for the email address in our DB
        # if the email is not in the database
            # create new user in DB
        # if the email IS in the database
            # flash message for this user already exists (or alert box?)

    user_email = request.form.get('user_email')
    user_password = request.form.get('user_password')

    if User.query.filter(User.email == user_email).first():
        return User.query.filter(User.email == user_email).one()
    else:
        new_user = User(email=user_email, password=user_password)
        db.session.add(new_user)
        db.session.commit()
        flash("User successfully added")
    
    return redirect("/")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
