import logging

import pydantic
import validators
from flask import Blueprint, abort, redirect, render_template, request
from sqlalchemy.exc import IntegrityError

from app import database, errors
from app.model import Url
from app.schema import Url_pydantic
from app.settings import Config

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/urls", methods=["POST"])
def create_url():
    try:
        url = Url_pydantic.model_validate_json(request.data)
        database.session.add(
            Url(**{"original_url": str(url.original_url), "short_url": url.short_url})
        )
        database.session.commit()
        logging.info("save {}", url.short_url)
        url.short_url = Config.DOMAIN_URL + "/" + url.short_url
        return url.model_dump()
    except (pydantic.ValidationError, validators.ValidationError) as e:
        logging.warning(e)
        abort(422, description="original url Validation error")
    except (IntegrityError, errors.IntegrityError) as e:
        logging.warning(e)
        abort(422, description="try again, this short url already exist")
    except errors.ValidationError as e:
        logging.warning(e)
        abort(422, description="short url Validation error")
    except Exception as e:
        logging.error(e)
        abort(400, description="big error")


@api.route("/<url>")
def redirect_index(url):
    return redirect("/")
