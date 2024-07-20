from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    education = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    experience = db.Column(db.String(200), nullable=True)
    additional_details = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(60), nullable=False)
<<<<<<< HEAD
    
    conversation_as_user1 = db.relationship('Conversation', foreign_keys='Conversation.user1_id', backref='user1', lazy=True)
    conversation_as_user2 = db.relationship('Conversation', foreign_keys='Conversation.user2_id', backref='user2', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

=======
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
>>>>>>> bf4b78e4a6b065271e2e5cf88d66e0ed3db5cb3f

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
<<<<<<< HEAD

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)  # Fixed typo

    def __repr__(self):
        return f"Message('{self.content}', '{self.date_sent}')"  # Fixed attribute names


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    messages = db.relationship('Message', backref='conversation', lazy=True)

    def __repr__(self):
        return f"Conversation('{self.id}', '{self.user1_id}', '{self.user2_id}')"
=======
    user = db.relationship('User', backref=db.backref('user_posts', lazy=True))
    likes = db.relationship('Like', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Nullable for non-authenticated users
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)  # To store IP address of the liker

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Nullable for non-authenticated users
    user = db.relationship('User', backref=db.backref('user_cmnt', lazy=True))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_name = db.Column(db.String(50), nullable=True)  # To store author name for non-authenticated users
>>>>>>> bf4b78e4a6b065271e2e5cf88d66e0ed3db5cb3f
