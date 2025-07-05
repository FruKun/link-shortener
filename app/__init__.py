from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from .database import database
from .error_handlers import error_handlers
from .settings import Config
from .views import api, web


def create_app(config=Config) -> Flask:
    app = Flask(__name__)
    cors = CORS(app)
    load_dotenv()
    app.config.from_object(config)
    database.init_app(app)
    with app.app_context():
        database.create_all()
    app.register_blueprint(web)
    app.register_blueprint(api)
    app.register_blueprint(error_handlers)
    return app
