from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

from . import errors

error_handlers = Blueprint("error_handlers", __name__)


@error_handlers.app_errorhandler(HTTPException)
def validation_handler(e):
    return jsonify(str(e)), e.code
