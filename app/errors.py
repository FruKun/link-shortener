from werkzeug.exceptions import HTTPException


class ValidationError(HTTPException):
    code = 422
    description = "Validation error try again"


class IntegrityError(HTTPException):
    code = 500
    description = "database error try again"
