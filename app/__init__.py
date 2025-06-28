from dotenv import load_dotenv
from flask import Flask

from .database import database
from .settings import Config
from .views import api, web


def create_app(config=Config) -> Flask:
    app = Flask(__name__)
    load_dotenv()
    app.config.from_object(config)
    database.init_app(app)
    app.register_blueprint(web)
    app.register_blueprint(api)
    return app
