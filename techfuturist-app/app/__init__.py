from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt  # <-- Ajout
from flask_mail import Mail
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))


load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
bcrypt = Bcrypt()  # <-- Instanciation
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SECRET_KEY'] = 'votre_clé_secrète_ultra_secrète'
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)  # <-- Initialisation
    mail.init_app(app)

    from app.routes import auth, dashboard, Home, admin, participant, resources, reports

    app.register_blueprint(Home.bp)

    app.register_blueprint(auth.bp)
    # app.register_blueprint(dashboard.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(resources.bp)
    app.register_blueprint(participant.bp)
    app.register_blueprint(reports.bp)
    

    return app
