from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from .settings import Config
from .views import api, web


class Base(DeclarativeBase):
    pass


database = SQLAlchemy(model_class=Base)


def create_app(config=Config) -> Flask:
    app = Flask(__name__)
    load_dotenv()
    app.config.from_object(config)
    database.init_app(app)
    app.register_blueprint(web)
    app.register_blueprint(api)
    return app
