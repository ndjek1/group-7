# app/auth.py
from datetime import datetime
from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from itsdangerous import URLSafeTimedSerializer # type: ignore
from app import db, bcrypt, mail
from app.forms import AdminLoginForm, AdminRegistrationForm, RegistrationForm, LoginForm
from app.models import Admin, User
from flask_mail import Mail, Message
from flask_login import login_user, current_user, logout_user, login_required # type: ignore

auth = Blueprint('auth', __name__)
@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and isinstance(current_user, User):
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.country_code.data + ' ' +form.phone_number.data,
            state=form.state.data,
            experience=form.experience.data,
            additional_details=form.additional_details.data
        )
        send_confirmation_email(user)
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! Please confirm your email to login', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@auth.route("/admin/register", methods=['GET', 'POST'])
def registerAdmin():
    if current_user.is_authenticated and isinstance(current_user, Admin):
        return redirect(url_for('main.admin'))
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password,
        )
        db.session.add(admin)
        db.session.commit()
        flash('Your admin account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.adminLogin'))
    return render_template('admin_register.html', title='Admin Register', form=form)

@auth.route("/admin/login", methods=['GET', 'POST'])
def adminLogin():
    if current_user.is_authenticated and isinstance(current_user, Admin):
        return redirect(url_for('main.admin'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.admin'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('admin_login.html', title='Admin Login', form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.confirmed:

            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        else:
            flash('You email is inactive please chexk your mail for confrimation email', 'danger')
            
    return render_template('login.html', title='Login', form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


def send_confirmation_email(user):
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('email_activate.html', confirm_url=confirm_url)
    msg = Message('Confirm Your Account', recipients=[user.email], html=html)
    try:
        mail.send(msg)
        print('Email sent successfully.')
    except Exception as e:
        print(f'Error sending email: {e}')

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

@auth.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.home'))


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
        return email
    except Exception:
        return False

