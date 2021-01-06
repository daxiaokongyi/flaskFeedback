from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm
from werkzeug.exceptions import Unauthorized 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///auth_user' 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def register():
    """Redirect to /register"""
    return redirect('/register')

@app.route("/register", methods=['GET', 'POST'])
def register_user():
    """Allows the user to register"""
    form = RegisterForm()
    if form.validate_on_submit():
        # data = {k: v for k,v in form.data.items() if k != 'csrf_token'}
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        flash("Welcome! Your account was successfully added")
        return redirect(f'/users/{new_user.username}')
    else:
        return render_template("register.html", form = form)

@app.route("/login", methods=['GET', 'POST'])
def login_user():
    """Allows the user to login """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user: 
            session['username'] = user.username
            flash(f"Welcome back, {user.username}!")
            return redirect(f'/users/{user.username}')
        else:
            # flash("Incorrect username or password. Please try again!")
            form.username.errors = ['Incorrect username or password. Please try again!']            
    return render_template('login.html', form = form)

@app.route("/logout")
def logout_user():
    """have user log out"""
    session.pop("username")
    flash("Successfully logged out")
    return redirect('/')

@app.route("/users/<username>")
def detail_user(username):
    """show the detail of the user"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()
        # flash("Sorry, you don't have permission to check this user's info.")
        # return redirect('/login')
    
    form = DeleteForm()

    user = User.query.get(session['username'])
    
    return render_template("detail.html", user = user, form = form)

@app.route("/users/<username>/delete")
def delete_user(username):
    """delete a user"""

    # check if the authorization
    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    user = User.query.get(username)
    session.pop("username")
    db.session.delete(user)
    db.session.commit()

    flash(message=f"{username} was deleted.")
    return redirect('/')

@app.route("/users/<username>/feedback/add", methods=['GET', 'POST'])
def feedback_user(username):
    """Add feedback for a certain user"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
        # flash("Sorry, you don't have permission to add a feedabck. Login first.")
        # return redirect('/login')

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title = title, content = content, username = username)
        db.session.add(new_feedback)
        db.session.commit()

        flash(message= "Feedback was added.")
        return redirect(f'/users/{username}')
    else:
        return render_template('feedback/add.html', form = form, username = username)

@app.route("/feedback/<int:feedback_id>/update", methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Update a feedback"""

    # get feedback
    feedback = Feedback.query.get_or_404(feedback_id)
    # check if the authorization
    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        flash(message="Feedback was updated.")
        return redirect(f'/users/{feedback.username}')
    else:
        return render_template(f'feedback/edit.html', form = form, feedback = feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=['Post'])
def delete_feedback(feedback_id):
    """Delete feedback"""
    feedback = Feedback.query.get(feedback_id)
    username = feedback.username 
    # check if the authorization
    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized()

    db.session.delete(feedback)
    db.session.commit()

    flash(message=f"Feedback was deleted.")
    return redirect(f'/users/{username}')

@app.errorhandler(404)
def invalid_route(e): 
    """handle error page"""
    return render_template('404.html'), 404