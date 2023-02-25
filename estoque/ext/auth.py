from flask import Flask
from flask_jwt_extended import JWTManager


def init_app(app: Flask) -> Flask:
    '''Inicia o JWT como extenção de JSON Web Tokens.'''
    JWTManager(app)
