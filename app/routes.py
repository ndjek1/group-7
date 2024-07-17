from flask import Blueprint, abort, app, flash, render_template, redirect, url_for, request,current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
import uuid
from app.forms import AnonymousCommentForm, CommentForm, LikeForm, PostForm, UpdateProfileForm
from sqlalchemy.orm import joinedload
import os

from app.models import Comment, Like, Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    posts = Post.query.limit(4).all()
    return render_template('home.html', posts = posts)

@main.route("/all_posts", methods=['GET', 'POST'])
def posts():
    posts = Post.query.all()

    return render_template('all_posts.html', posts=posts)

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

def save_picture(form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = secure_filename(current_user.username + f_ext)
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn




def save_post_picture(form_picture):
    unique_id = uuid.uuid4().hex
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = secure_filename(current_user.username + unique_id + f_ext)
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@main.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_file = save_post_picture(form.image_file.data)
            post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id,user= current_user, image_file=image_file)
        else:
            post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id, user = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form)

@main.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    if current_user.is_authenticated:
        form = CommentForm()
    else:
        form = AnonymousCommentForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(content=form.content.data, post_id=post_id, user_id=current_user.id)
        else:
            comment = Comment(content=form.content.data, post_id=post_id, author_name=form.name.data)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('main.post', post_id=post_id))

    return render_template('post.html', title=post.title, post=post, comments=comments, form=form)

@main.route("/like/<int:post_id>", methods=['GET','POST'])
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    ip_address = request.remote_addr

    if current_user.is_authenticated:
        like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
        if like:
            db.session.delete(like)
        else:
            new_like = Like(user_id=current_user.id, post_id=post_id)
            db.session.add(new_like)
    else:
        like = Like.query.filter_by(ip_address=ip_address, post_id=post_id).first()
        if like:
            db.session.delete(like)
        else:
            new_like = Like(ip_address=ip_address, post_id=post_id)
            db.session.add(new_like)

    db.session.commit()
    return redirect(url_for('main.posts'))



@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
