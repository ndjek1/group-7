from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.forms import UpdateProfileForm
import os

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')


@main.route("/profile", methods=['GET', 'POST'])  # Add POST method to the route
@login_required
def profile():
    form = UpdateProfileForm()
    
    if form.validate_on_submit():
        # Update user details
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.education = form.education.data
        current_user.country = form.country.data
        current_user.state = form.state.data
        current_user.experience = form.experience.data
        current_user.additional_details = form.additional_details.data
        
        # Handle profile picture upload
        if form.picture.data:
            image_file = save_picture(form.picture.data)
            current_user.image_file = image_file
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))  # Corrected to 'main.profile'
    
    # Populate form fields with current user data
    form.email.data = current_user.email
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.phone.data = current_user.phone
    form.address.data = current_user.address
    form.education.data = current_user.education
    form.country.data = current_user.country
    form.state.data = current_user.state
    form.experience.data = current_user.experience
    form.additional_details.data = current_user.additional_details
    
    return render_template('profile.html', title='Profile', form=form)

@main.route("/opportunities")
def opportunities():
    return render_template('opportunities.html')

def save_picture(form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = secure_filename(current_user.username + f_ext)
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn
