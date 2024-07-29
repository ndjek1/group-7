from flask import Blueprint, abort, flash, render_template, redirect, url_for, request, current_app # type: ignore
from flask_login import login_required, current_user # type: ignore
from werkzeug.utils import secure_filename # type: ignore
from app import db
from app.forms import DonationForm, Event_registration, UpdateProfileForm, MessageForm
from app.models import Admin, Follow, User, Conversation, Message
from app.utils import read_event_registrations, register_attendees

from flask import Blueprint, abort, app, flash, render_template, redirect, url_for, request,current_app # type: ignore
from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app # type: ignore

from flask_login import login_required, current_user # type: ignore
from werkzeug.utils import secure_filename # type: ignore
from app import db
import uuid
from app.forms import  CommentForm, PostForm, UpdateProfileForm
from flask import jsonify
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
    likes = []
    if current_user.is_authenticated:
        likes = [like.post_id for like in Like.query.filter_by(user_id=current_user.id).all()]
    return render_template('home.html', posts = posts, news = news, events = events, likes = likes)


@main.route("/admin")
def admin():
    posts = Post.query.filter_by(category='post').all()
    news = Post.query.filter_by(category='news').all()
    events = Post.query.filter_by(category='event').all()
    event_registrations = read_event_registrations()
    if current_user.is_authenticated:
        return render_template('admin.html', posts = posts, news = news, events = events, event_registrations = event_registrations)
    return redirect(url_for('auth.adminLogin'))

@main.route("/all_posts", methods=['GET', 'POST'])
def posts():
    posts = Post.query.all()

    return render_template('all_posts.html', posts=posts)


@main.route("/profile/<int:user_id>", methods=['GET', 'POST'])
@login_required
def profile(user_id):
    form = UpdateProfileForm()
    is_current_user = (current_user.id == user_id)
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
        return redirect(url_for('main.profile',user_id=current_user.id))

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

    return render_template('profile.html', title='Profile', form=form, user=current_user, is_current_user=is_current_user, user_id=user_id)

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
    is_current_user = (user_id == current_user.id)
    is_following = Follow.query.filter_by(follower_id=current_user.id, followee_id=user.id).first() is not None
    form = MessageForm()

    if form.validate_on_submit():
        print("Form submitted and validated!")  # Debug statement
        message_text = form.message.data
        new_message = Message(sender_id=current_user.id, receiver_id=user_id, message=message_text)
        db.session.add(new_message)
        db.session.commit()
        flash('Message sent!', 'success')
        return redirect(url_for('main.view_user_profile', user_id=user_id))

    return render_template('profile.html', user=user, is_current_user=is_current_user, form=form, is_following = is_following)

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
    followed_users = [follow.followee for follow in user.following]

    # Ensure user2 is defined correctly
    for conversation in conversations:
        
        last_message = Message.query.filter_by(conversation_id=conversation.id).order_by(Message.date_sent.desc()).first()
        conversation.last_message = last_message
        if conversation.user1_id == user.id:
            conversation.user2 = User.query.get(conversation.user2_id)
        else:
            # Swap user1 and user2 to make current user always user1
            conversation.user2 = User.query.get(conversation.user1_id)
            conversation.user1_id = user.id
            conversation.user2_id = conversation.user2.id

    return render_template('conversations_list.html', conversations=conversations, followed_users = followed_users)


@conversations.route("/start_conversation/<int:user_id>", methods=['GET', 'POST'])
@login_required
def start_conversation(user_id):
    user2 = User.query.get_or_404(user_id)
    
    # Check if both users are following each other
    is_following_user2 = Follow.query.filter_by(follower_id=current_user.id, followee_id=user2.id).first()
    is_followed_by_user2 = Follow.query.filter_by(follower_id=user2.id, followee_id=current_user.id).first()
    
    if not is_following_user2 or not is_followed_by_user2:
        flash("You and the other user need to follow each other before starting a conversation.", "warning")
        return redirect(url_for('conversations.conversations_list'))  # Redirect to an appropriate view
    
    # Check if conversation already exists
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
        admin = Admin.query.get_or_404(current_user.email)
        if admin:
            if form.image_file.data:
                image_file = save_post_picture(form.image_file.data)
                
                post = Post(
                    title=form.title.data, 
                    content=form.content.data,
                    link=form.link.data,
                    category=form.category.data, 
                    user_id=current_user.id, 
                    image_file=image_file
                )
            else:
                post = Post(
                    title=form.title.data, 
                    content=form.content.data,
                    link=form.link.data,
                    category=form.category.data, 
                    user_id=current_user.id
                )
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
        else:
            flash('Sorry only administrators are allowed to post', 'success')
        return redirect(url_for('main.admin'))
    return render_template('create_post.html', title='New Post', form=form)

@main.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    
    form = CommentForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(content=form.content.data, post_id=post_id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('main.post', post_id=post_id))

    return render_template('post.html', title=post.title, post=post, comments=comments, form=form)

@main.route("/like/<int:post_id>", methods=['POST','GET'])
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    ip_address = request.remote_addr
    was_liked = False

    if current_user.is_authenticated:
        existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
        if existing_like:
            db.session.delete(existing_like)
            was_liked = False
        else:
            new_like = Like(user_id=current_user.id, post_id=post_id)
            db.session.add(new_like)
            was_liked = True
    else:
        existing_like = Like.query.filter_by(ip_address=ip_address, post_id=post_id).first()
        if existing_like:
            db.session.delete(existing_like)
            was_liked = False
        else:
            new_like = Like(ip_address=ip_address, post_id=post_id)
            db.session.add(new_like)
            was_liked = True

    db.session.commit()
    return jsonify(success=True, liked=was_liked)




@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_file = save_post_picture(form.image_file.data)
            post.image_file = image_file
        post.title = form.title.data
        post.content = form.content.data
        post.link = form.link.data
        post.category = form.category.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.admin'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.link.data = post.link
        form.category.data = post.category
    return render_template('create_post.html', title='Update Post', form=form, post=post)

@main.route("/post/<int:post_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.admin'))


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



@main.route('/follow/<int:followee_id>', methods=['POST'])
@login_required
def follow_user(followee_id):
    follower_id = current_user.id
    if follower_id == followee_id:
        flash('You cannot follow yourself.', 'warning')
        return redirect(url_for('main.profile', user_id=followee_id))
    
    follow = Follow.query.filter_by(follower_id=follower_id, followee_id=followee_id).first()
    if not follow:
        new_follow = Follow(follower_id=follower_id, followee_id=followee_id)
        db.session.add(new_follow)
        db.session.commit()
        flash('You are now following this user.', 'success')
    else:
        flash('You are already following this user.', 'info')
    
    return redirect(url_for('main.view_user_profile', user_id=followee_id))

@main.route('/unfollow/<int:followee_id>', methods=['POST'])
@login_required
def unfollow_user(followee_id):
    follower_id = current_user.id
    follow = Follow.query.filter_by(follower_id=follower_id, followee_id=followee_id).first()
    if follow:
        db.session.delete(follow)
        db.session.commit()
        flash('You have unfollowed this user.', 'success')
    else:
        flash('You are not following this user.', 'info')
    
    return redirect(url_for('main.view_user_profile', user_id=followee_id))

@main.route("/register/<int:event_id>", methods=['GET', 'POST'])
def register_for_event(event_id):
    event = Post.query.get_or_404(event_id)
    form = Event_registration()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        event_name = event.title
        register_attendees(full_name, email, event_name)
        flash('Thank you for registering for this event! Best regards', 'success')
        return redirect(url_for('auth.login'))
    return render_template('event_registration.html', title='Event Registration', form=form, event_id = event_id )


@main.route("/donate", methods=['GET', 'POST'])
def donate():
    form = DonationForm()
    if form.validate_on_submit():
        amount = form.amount.data
        payment_method = request.form.get('payment_method')
        phone_number = form.phone_number.data if payment_method in ['mobile_money', 'airtel_money'] else None
        card_number = form.card_number.data if payment_method == 'visa' else None
        card_name = form.card_name.data if payment_method == 'visa' else None
        expiry_date = form.expiry_date.data if payment_method == 'visa' else None
        cvv = form.cvv.data if payment_method == 'visa' else None

        # Process the donation based on the payment method
        if payment_method == 'visa':
            # Process Visa payment
            flash('Visa payment processed successfully.', 'success')
        elif payment_method in ['mobile_money', 'airtel_money']:
            # Process Mobile Money or Airtel Money payment
            flash('Mobile Money/Airtel Money payment processed successfully.', 'success')
        else:
            flash('Invalid payment method.', 'danger')
        
        return redirect(url_for('main.home'))
    return render_template('donate.html', title='Donate', form=form)

@main.route('/search')
def search():
    keyword = request.args.get('keyword')
    if keyword:
        # Perform search using the keyword
        users = User.query.filter(User.first_name.ilike(f'%{keyword}%')).all() or User.query.filter(User.last_name.ilike(f'%{keyword}%')).all()
    else:
        users = []
    
    return render_template('search_result.html', users=users)