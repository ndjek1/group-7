# app/forms.py
import re
from flask_wtf import FlaskForm # type: ignore
from wtforms import DecimalField, FileField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField # type: ignore
from wtforms import FileField, IntegerField,TextAreaField, StringField, PasswordField, SubmitField, BooleanField, SelectField # type: ignore
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional # type: ignore
from app.models import User
from flask_wtf.file import FileAllowed # type: ignore
from app.utils import load_allowed_users

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError, NumberRange
import re

from app.utils import load_allowed_users

class RegistrationForm(FlaskForm):

    username = StringField(
        'Username', 
        validators=[
            DataRequired(message="Username is required."), 
            Length(min=2, max=20, message="Username must be between 2 and 20 characters.")
        ]
    )
    email = StringField(
        'Email', 
        validators=[
            DataRequired(message="Email is required."), 
            Email(message="Enter a valid email address.")
        ]
    )
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, message="Password must be at least 6 characters long.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[
            DataRequired(message="Please confirm your password."), 
            EqualTo('password', message="Passwords must match.")
        ]
    )
    role = SelectField('Role', choices=[
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee'),
    ], validators=[DataRequired()])

    first_name = StringField(
        'First Name', 
        validators=[
            Optional()
        ]
    )
    last_name = StringField(
        'Last Name', 
        validators=[
            Optional()
        ]
    )
    student_number = StringField(
        'Student Number',
        validators=[
            DataRequired(message="Student Number is required."),
            Length(min=10, max=10, message="Student Number must be 10 digits long."),
        ]  
    )
   
    country_code = SelectField(
        'Country', 
        choices=[
            ('+256', '(Uganda)'),
            ('+254', ' (Kenya)'),
            ('+255', ' (Tanzania)'),
            ('+250', '(Rwanda)'),
            ('+257', '(Burundi)'),
            ('+211', '(South Sudan)'),
            ('+251', '(Ethiopia)'),
            ('+252', '(Somalia)'),
            ('+249', '(Sudan)'),
            ('+1', '(United States)'),
            ('+91', '(India)'),
            ('+44', ' (United Kingdom)'),
            ('+27', '(South Africa)'),
            ('+234', '(Nigeria)'),
            ('+233', '(Ghana)'),
            ('+20', '(Egypt)')
        ], 
        validators=[Optional()]
    )
    
    phone_number = StringField(
        'Phone', 
        validators=[Optional()]
    )
    state = StringField('State', validators=[Optional(), Length(max=50)])
    experience = StringField('Experience', validators=[Optional(), Length(max=200)])
    additional_details = StringField('Additional Details', validators=[Optional(), Length(max=200)])
    
    submit = SubmitField('Sign Up')

    def validate_phone_number(self, phone_number):
        # Ensure that the phone number has exactly 10 digits
        if not re.match(r'^\d{10}$', phone_number.data):
            raise ValidationError('Phone number must be exactly 10 digits.')

    def validate_student_number(self, student_number):
        allowed_users = load_allowed_users('app/data.csv')
        if student_number.data not in allowed_users:
            raise ValidationError('Student number does not match our records.')

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

class Event_registration(FlaskForm):
    full_name = StringField('Full name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

class DonationForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    phone_number = StringField('Phone Number')
    card_number = StringField('Card Number')
    card_name = StringField('Name on Card')
    expiry_date = StringField('Expiry Date')
    cvv = StringField('CVV')
    submit = SubmitField('Donate')