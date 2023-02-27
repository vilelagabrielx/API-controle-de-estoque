from flask_sqlalchemy import SQLAlchemy
from flask import Flask
db = SQLAlchemy()


def init_app(app: Flask):
    '''Inicia o SQLAlchemy como ORM.'''
    db.init_app(app)
