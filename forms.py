from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

class RegisterForm(FlaskForm):
    """Registration Form"""
    username = StringField("User Name", validators=[InputRequired(message = "User name is required")])
    password = PasswordField("Password", validators=[InputRequired(message = "Password is required")]) 
    email = StringField("Email", validators=[InputRequired(message = "Email is required"), Email()])
    first_name = StringField("First Name", validators=[InputRequired(message = "First name is required")])
    last_name = StringField("Last Name", validators=[InputRequired(message = "Last name is required")])

class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField("User Name", validators=[InputRequired(message = "User name is required")])
    password = PasswordField("Password", validators=[InputRequired(message = "Password is required")]) 

class FeedbackForm(FlaskForm):
    """Feedback Form"""
    title = StringField("Title", validators=[InputRequired(message = "Title is required"), Length(max = 100)])
    content = StringField("Content", validators=[InputRequired(message = "Content is required")])

class DeleteForm(FlaskForm):
    """Delete Form"""