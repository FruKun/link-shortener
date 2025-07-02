from http.client import responses

from flask import Blueprint, render_template
from werkzeug.exceptions import HTTPException

error_handlers = Blueprint("error_handlers", __name__)


@error_handlers.app_errorhandler(HTTPException)
def validation_handler(e):
    return (
        render_template(
            "modules/response_error.html",
            code=responses.get(e.code, "Unknown Error"),
            description=e.description,
        ),
        e.code,
    )
