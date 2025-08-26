import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    
    # --- DEBUT DE LA MODIFICATION POUR LE DEPLOIEMENT ---
    # Configuration intelligente de la base de données
    if 'PYTHONANYWHERE_USER' in os.environ:
        # Chemin absolu et complet pour le serveur PythonAnywhere
        db_path = f"/home/{os.environ['PYTHONANYWHERE_USER']}/Translator/instance/translation_app.db"
        # Crée le dossier 'instance' sur le serveur s'il n'existe pas
        os.makedirs(f"/home/{os.environ['PYTHONANYWHERE_USER']}/Translator/instance", exist_ok=True)
    else:
        # Chemin relatif qui fonctionne sur ton PC local
        basedir = os.path.abspath(os.path.dirname(__file__))
        # Crée le dossier 'instance' localement s'il n'existe pas
        os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
        db_path = os.path.join(basedir, 'instance', 'translation_app.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    # --- FIN DE LA MODIFICATION POUR LE DEPLOIEMENT ---

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["UPLOAD_FOLDER"] = "uploads"
    app.config["PROFILE_PHOTOS_FOLDER"] = "static/profile_photos"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
    
    # Create upload directories
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["PROFILE_PHOTOS_FOLDER"], exist_ok=True)
    
    # ProxyFix for HTTPS
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # type: ignore
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'info'
    
    # Import models and routes
    from models import User, Translation
    from routes import register_blueprints
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    register_blueprints(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

# Create the app instance
app = create_app()
