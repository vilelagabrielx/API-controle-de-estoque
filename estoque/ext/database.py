from flask_sqlalchemy import SQLAlchemy
from flask import Flask
db = SQLAlchemy()


def init_app(app: Flask) -> Flask:
    db.init_app(app)
