from flask_socketio import SocketIO # type: ignore
from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_bcrypt import Bcrypt # type: ignore
from flask_login import LoginManager, current_user # type: ignore
from flask_migrate import Migrate # type: ignore
from flask_wtf.csrf import CSRFProtect

socketio = SocketIO()

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '2607/favy'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['DEBUG'] = True  
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
