from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from app.database import database
from app.model import Url
from app.service import validate_original_url, validate_short_url
from app.settings import Config

from . import errors


class Url_pydantic(BaseModel):
    original_url: Annotated[str, BeforeValidator(validate_original_url)]
    short_url: Annotated[
        str,
        Field(default=None, validate_default=True),
        BeforeValidator(validate_short_url),
    ]

    model_config = ConfigDict(from_attributes=True)
