# app/forms.py
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms import FileField, IntegerField,TextAreaField, StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from app.models import User
from flask_wtf.file import FileAllowed

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
    first_name = StringField(
        'First Name', 
        validators=[
            DataRequired(message="First name is required.")
        ]
    )
    last_name = StringField(
        'Last Name', 
        validators=[
            DataRequired(message="Last name is required.")
        ]
    )
   
    country = SelectField(
        'Country', 
        choices=[
            ('UG', '+256 (Uganda)'),
            ('KE', '+254 (Kenya)'),
            ('TZ', '+255 (Tanzania)'),
            ('RW', '+250 (Rwanda)'),
            ('BI', '+257 (Burundi)'),
            ('SS', '+211 (South Sudan)'),
            ('ET', '+251 (Ethiopia)'),
            ('SO', '+252 (Somalia)'),
            ('SD', '+249 (Sudan)'),
            ('US', '+1 (United States)'),
            ('IN', '+91 (India)'),
            ('UK', '+44 (United Kingdom)'),
            ('ZA', '+27 (South Africa)'),
            ('NG', '+234 (Nigeria)'),
            ('GH', '+233 (Ghana)'),
            ('EG', '+20 (Egypt)')
        ], 
        validators=[DataRequired(message="Country code is required.")]
    )
    
    phone = StringField(
        'Phone', 
        validators=[
            DataRequired(message="Phone number is required.")
        ]
    )
    
    additional_details = StringField(
        'Additional Details'
    )
    submit = SubmitField('Sign Up')

    def validate_phone(self, phone):
        # Ensure that the phone number has exactly 10 digits
        if not re.match(r'^\d{10}$', phone.data):
            raise ValidationError('Phone number must be exactly 10 digits.')


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