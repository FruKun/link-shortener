import logging

from flask import Blueprint, render_template, request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app import errors
from app.database import database
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
        url.short_url = Config.DOMAIN_URL + "/" + url.short_url
        responce = url.dict()
    except ValidationError as e:
        # 422
        logging.error(e)
        responce = "original url Validation error"
    except errors.ValidationError:
        # 422
        logging.error("errors.ValidationError: short url Validation error")
        responce = "short url Validation error"
    except IntegrityError as e:
        # 422
        logging.error(e)
        responce = "try again, this short url already exist"
    except errors.IntegrityError as e:
        # 422
        logging.error("errors.IntegrityError: dont unique value")
        responce = "try again, this short url already exist"
    except Exception as e:
        # 400
        logging.error(e)
        responce = "big error"
    return responce


@api.route("/doc", methods=["GET"])
def get_doc_url():
    return render_template("doc.html")
