from flask import Flask, url_for, render_template
from flask_mail import Mail, Message
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from app.utils import load_allowed_users

socketio = SocketIO()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '2607/favy'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECURITY_PASSWORD_SALT']='fkslkfsdlkfnsdfnsfd'
    app.config['MAIL_SERVER'] = 'email-smtp.us-east-2.amazonaws.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_DEFAULT_SENDER'] = 'vndjekornom@gmail.com'  # Your SES SMTP username
    app.config['MAIL_USERNAME'] = 'AKIAZQ3DQ3AK46QXN3V7'  # Your SES SMTP username
    app.config['MAIL_PASSWORD'] = 'BDERfjga12b5sG6Z+0Blnj0hf9E5vX0dHsS9D+tWzwyt'  # Your SES SMTP password
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['DEBUG'] = True

    mail.init_app(app)
    csrf = CSRFProtect(app)
    socketio.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.routes import messages as messages_blueprint
    app.register_blueprint(messages_blueprint)

    from app.routes import conversations as conversations_blueprint
    app.register_blueprint(conversations_blueprint)

    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    return app
