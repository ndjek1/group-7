from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin # type: ignore

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(120), unique=False, nullable=True, default='mentee')
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
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    user_posts = db.relationship('Post', foreign_keys='Post.user_id', overlaps="author,posts")
    user_cmnt = db.relationship('Comment', foreign_keys='Comment.user_id', overlaps="author,comments")
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)

    conversations_as_user1 = db.relationship('Conversation', foreign_keys='Conversation.user1_id', backref='user1_ref', lazy=True)
    conversations_as_user2 = db.relationship('Conversation', foreign_keys='Conversation.user2_id', backref='user2_ref', lazy=True)

    followers = db.relationship('Follow', backref='followee', foreign_keys='Follow.followee_id', lazy=True)
    following = db.relationship('Follow', backref='follower', foreign_keys='Follow.follower_id', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Ensuring that the same follower cannot follow the same followee more than once
    __table_args__ = (db.UniqueConstraint('follower_id', 'followee_id', name='unique_follow'),)

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('Like', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)
    link = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(25), nullable=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)

    def __repr__(self):
        return f"Message('{self.content}', '{self.date_sent}')"

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    messages = db.relationship('Message', backref='conversation', lazy=True)

    def __repr__(self):
        return f"Conversation('{self.id}', '{self.user1_id}', '{self.user2_id}')"

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Nullable for non-authenticated users
    user = db.relationship('User', foreign_keys=user_id, overlaps="author,comments")
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_name = db.Column(db.String(50), nullable=True)  # To store author name for non-authenticated users
