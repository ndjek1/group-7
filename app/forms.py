# app/forms.py
from flask_wtf import FlaskForm # type: ignore
from wtforms import FileField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField # type: ignore
from wtforms import FileField, IntegerField,TextAreaField, StringField, PasswordField, SubmitField, BooleanField, SelectField # type: ignore
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional # type: ignore
from app.models import User
from flask_wtf.file import FileAllowed # type: ignore

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee')
    ], validators=[DataRequired()])
    # New fields
    first_name = StringField('First Name', validators=[Optional(), Length(max=30)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=30)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    address = StringField('Address', validators=[Optional(), Length(max=100)])
    education = StringField('Education', validators=[Optional(), Length(max=100)])
    country = StringField('Country', validators=[Optional(), Length(max=50)])
    state = StringField('State', validators=[Optional(), Length(max=50)])
    experience = StringField('Experience', validators=[Optional(), Length(max=200)])
    additional_details = StringField('Additional Details', validators=[Optional(), Length(max=200)])
    
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        
class AdminRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Add')

class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    phone = StringField('Phone', validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    education = StringField('Education', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])
    state = StringField('State', validators=[Optional()])
    experience = StringField('Experience in Designing')
    additional_details = StringField('Additional Details')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Save Profile')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    link = TextAreaField('Link', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('post', 'Post'),
        ('event', 'Event'),
        ('news', 'News')
    ], validators=[Optional()])
    image_file = FileField('Image', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Publish')

class CommentForm(FlaskForm):
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class AnonymousCommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class LikeForm(FlaskForm):
    submit = SubmitField('Like')

class MessageForm(FlaskForm):
    
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('send')