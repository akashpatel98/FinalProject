from flask import Flask
from flask_assests import Environment
from .assets import compile_assets


# Globally accessible libraries
db = SQLAlchemy()
r = FlaskRedis()
assets = Environment()


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
     """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
     app.config.from_object('config.Config')

     # Initialize plugins
    assets.init_app(app)

    with app.app_context():
    # Import parts of our application
     from .admin import routes
     from .main importn routes
    app.register_blueprint(admin_routes.admin_bp)
    app.register_blueprint(main_routes.main_bp)
     compile_assets(assets)

        return app