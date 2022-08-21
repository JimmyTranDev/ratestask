from flask import request, jsonify, Blueprint, current_app
from ratestask.validators import validate_rates_queries
from ratestask.db import Database
from flask.wrappers import Response
from typing import TypedDict


class DayRate(TypedDict):
    day: str
    average_price: int


api = Blueprint("api", __name__)


@api.get("/rates")
@validate_rates_queries
def get_rates() -> Response:
    """API to get daily average price rates between two ports/destiantions"""

    # Get Database
    db: Database = current_app.db

    # Get query params for api
    date_from: str = request.args.get("date_from")
    date_to: str = request.args.get("date_to")
    origin: str = request.args.get("origin")
    destination: str = request.args.get("destination")

    # Gets reults from database
    rates_result = db.get_rates(date_from, date_to, origin, destination)

    # Converts sql result to dto
    def rates_dto(data: list[str]) -> DayRate:
        day: str = data[0]
        average_price: str = data[1]
        average_price: int = round(average_price) if average_price else average_price
        return {"day": day.strftime("%Y-%m-%d"), "average_price": average_price}

    results = [rates_dto(x) for x in rates_result]

    return jsonify(results)
