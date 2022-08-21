from flask import request, jsonify
from marshmallow import Schema, fields, ValidationError
from functools import wraps

DEFAULT_DATE_FMT = "%Y-%m-%d"


class RatesQuerySchema(Schema):
    date_from = fields.Date(required=True, format=DEFAULT_DATE_FMT)
    date_to = fields.Date(required=True, format=DEFAULT_DATE_FMT)
    origin = fields.Str(required=True)
    destination = fields.Str(required=True)


def validate_rates_queries(f):
    """Decorator that validates GET rates api query params"""

    @wraps(f)
    def decorated(*args, **kwargs):
        argsDict = {key: val for key, val in request.args.items()}
        try:
            RatesQuerySchema().load(argsDict)

            # date_from > date_to always returns an empty list (Likely input error)
            if argsDict["date_from"] > argsDict["date_to"]:
                raise ValidationError("date_from larger than date_to")
        except ValidationError as err:
            return (
                jsonify(message="Bad Request", queries=argsDict, errors=err.messages),
                400,
            )
        return f(*args, **kwargs)

    return decorated
