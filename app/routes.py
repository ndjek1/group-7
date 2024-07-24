from flask import Blueprint, abort, flash, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.forms import UpdateProfileForm, MessageForm
from app.models import User, Conversation, Message

from flask import Blueprint, abort, app, flash, render_template, redirect, url_for, request,current_app

from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
import uuid
from app.forms import AnonymousCommentForm, CommentForm, LikeForm, PostForm, UpdateProfileForm
from sqlalchemy.orm import joinedload
import os

from app.models import Comment, Like, Post

from app import db, socketio
from flask_socketio import emit, join_room, leave_room # type: ignore

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    posts = Post.query.filter_by(category='post').all()
    news = Post.query.filter_by(category='news').all()
    events = Post.query.filter_by(category='event').all()
    return render_template('home.html', posts = posts, news = news, events = events)


@main.route("/admin")
def admin():
    posts = Post.query.filter_by(category='post').all()
    news = Post.query.filter_by(category='news').all()
    events = Post.query.filter_by(category='event').all()
    if current_user.is_authenticated:
        return render_template('admin.html', posts = posts, news = news, events = events)
    return redirect(url_for('auth.adminLogin'))

@main.route("/all_posts", methods=['GET', 'POST'])
def posts():
    posts = Post.query.all()

    return render_template('all_posts.html', posts=posts)


@main.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()

    if form.validate_on_submit():
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

        if form.picture.data:
            image_file = save_picture(form.picture.data)
            current_user.image_file = image_file

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))

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

    is_current_user = True

    return render_template('profile.html', title='Profile', form=form, user=current_user, is_current_user=is_current_user)

@main.route('/users')
@login_required
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@main.route("/opportunities")
def opportunities():
    return render_template('opportunities.html')

def save_picture(form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = secure_filename(current_user.username + f_ext)
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@main.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def view_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    form = MessageForm()

    if form.validate_on_submit():
        print("Form submitted and validated!")  # Debug statement
        message_text = form.message.data
        new_message = Message(sender_id=current_user.id, receiver_id=user_id, message=message_text)
        db.session.add(new_message)
        db.session.commit()
        flash('Message sent!', 'success')
        return redirect(url_for('main.view_user_profile', user_id=user_id))

    is_current_user = (current_user.id == user_id)
    return render_template('profile.html', user=user, is_current_user=is_current_user, form=form)

conversations = Blueprint('conversations', __name__)



@conversations.route('/conversation/<int:conversation_id>', methods=['GET', 'POST'])
@login_required
def view_conversation(conversation_id):
    conversation = Conversation.query.get_or_404(conversation_id)
    
    # Ensure user1 is the current user
    if conversation.user1_id == current_user.id:
        user1 = current_user
        user2 = User.query.get_or_404(conversation.user2_id)
    else:
        user1 = current_user
        user2 = User.query.get_or_404(conversation.user1_id)
        # Swap user1 and user2 to make current user always user1
        conversation.user1_id = current_user.id
        conversation.user2_id = user2.id

    if conversation.user1_id != current_user.id and conversation.user2_id != current_user.id:
        abort(403)

    form = MessageForm()
    if form.validate_on_submit():
        message = Message(content=form.content.data, sender_id=current_user.id, conversation_id=conversation.id)
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent!', 'success')
        return redirect(url_for('conversations.view_conversation', conversation_id=conversation.id))

    messages = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.date_sent).all()
    return render_template('conversation.html', conversation=conversation, messages=messages, form=form, user1=user1, user2=user2, conversation_id=conversation.id)
@conversations.route("/conversations")
@login_required
def conversations_list():
    user = current_user
    conversations = Conversation.query.filter(
        (Conversation.user1_id == user.id) | (Conversation.user2_id == user.id)
    ).all()

    # Ensure user2 is defined correctly
    for conversation in conversations:
        if conversation.user1_id == user.id:
            conversation.user2 = User.query.get(conversation.user2_id)
        else:
            # Swap user1 and user2 to make current user always user1
            conversation.user2 = User.query.get(conversation.user1_id)
            conversation.user1_id = user.id
            conversation.user2_id = conversation.user2.id

    return render_template('conversations_list.html', conversations=conversations)


@conversations.route("/start_conversation/<int:user_id>", methods=['GET', 'POST'])
@login_required
def start_conversation(user_id):
    user2 = User.query.get_or_404(user_id)
    conversation = Conversation.query.filter(
        ((Conversation.user1_id == current_user.id) & (Conversation.user2_id == user2.id)) |
        ((Conversation.user1_id == user2.id) & (Conversation.user2_id == current_user.id))
    ).first()

    if not conversation:
        conversation = Conversation(user1_id=current_user.id, user2_id=user2.id)
        db.session.add(conversation)
        db.session.commit()

    return redirect(url_for('conversations.view_conversation', conversation_id=conversation.id))


messages = Blueprint('messages', __name__)

@messages.route('/messages', methods=['GET', 'POST'])
@login_required
def message_list():
    form = MessageForm()

    if form.validate_on_submit():
        receiver_id = form.receiver_id.data
        message_text = form.message.data
        new_message = Message(sender_id=current_user.id, receiver_id=receiver_id, message=message_text)
        db.session.add(new_message)
        db.session.commit()
        flash('Message sent!', 'success')
        return redirect(url_for('messages.message_list'))

    received_messages = Message.query.filter_by(receiver_id=current_user.id).all()
    sent_messages = Message.query.filter_by(sender_id=current_user.id).all()

    return render_template('messages.html', received_messages=received_messages, sent_messages=sent_messages, form=form)



def save_post_picture(form_picture):
    unique_id = uuid.uuid4().hex
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = secure_filename(current_user.username + unique_id + f_ext)
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@main.route("/admin/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_file = save_post_picture(form.image_file.data)
            post = Post(title=form.title.data, content=form.content.data,link = form.link.data,category = form.category.data, user_id=current_user.id, image_file=image_file)
        else:
            post = Post(title=form.title.data, content=form.content.data,link= form.link.data,category = form.category.data, user_id=current_user.id, user = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.admin'))
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


# SocketIO Events
@socketio.on('send_message')
def handle_send_message(data):
    message = Message(content=data['message'], sender_id=data['sender_id'], conversation_id=data['conversation_id'])
    db.session.add(message)
    db.session.commit()
    data['timestamp'] = message.date_sent.strftime('%Y-%m-%d %H:%M:%S')
    emit('receive_message', data, room=data['conversation_id'])

@socketio.on('join')
def handle_join(data):
    join_room(data['conversation_id'])

@socketio.on('leave')
def handle_leave(data):
    leave_room(data['conversation_id'])

