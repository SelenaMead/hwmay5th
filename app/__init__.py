from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager



db = SQLAlchemy()
migrate = Migrate()
login = LoginManager() 


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    

    db.init_app(app) 
    migrate.init_app(app, db) 
    login.init_app(app)
   
    



    with app.app_context():
        from app.blueprints import bp as main_bp
        app.register_blueprint(main_bp)

    

    return app