from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "QuestionManagement.db"

def create_app():
    app = Flask(__name__)
    #app.config.from_pyfile('config.py')
    #app.config['APPLICATION_ROOT'] = '/manager'
    app.config['SECRET_KEY'] = '6s54da98sd4q6w54edq6847a6g5d4g9'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .api import api_bp

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/')
    
    from .models import User, Sector

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
        
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Banco de dados criado!')


