from flask import Flask
from flask_migrate import Migrate
from database.db import db
from routes.contact_routes import contact_bp
from routes.main_routes import main_bp
# babel = Babel()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    # Initialize DB
    db.init_app(app)
    migrate.init_app(app, db)
    # Register Blueprints
    app.register_blueprint(main_bp)

    app.register_blueprint(contact_bp)

    return app
