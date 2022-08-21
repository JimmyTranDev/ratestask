import sys

# Adds current dir to python path or else modulentofounderror
sys.path.append(".")

from dotenv import load_dotenv
from flask import Flask
from ratestask.api import api
from ratestask.db import Database
from psycopg2 import OperationalError
import time

load_dotenv()


def create_app() -> None:
    app = Flask(__name__)
    app.register_blueprint(api)
    try:
        app.db = Database()
    except OperationalError:
        print("Database connection failed. Retrying in 1s...")
        time.sleep(1)
        return create_app()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
