from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# Globally accessible libraries
db = SQLAlchemy()
r = FlaskRedis()
assets = Environment()

ddb = SQLAlchemy()
login_manager = LoginManager()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    r.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import routes

        # Register Blueprints
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(admin.admin_bp)
        assets = Environment()


def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import routes
        from . import auth
        from .assets import compile_assets

        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        # Create Database Models
        db.create_all()

        # Compile static assets
        if app.config['FLASK_ENV'] == 'development':
            compile_assets(app)

        return app