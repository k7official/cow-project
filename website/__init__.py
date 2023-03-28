from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'database2.db'


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .models import Cow, Img

    create_database(app)

    return app


def create_database(app):
    if not path.exists('website' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')

