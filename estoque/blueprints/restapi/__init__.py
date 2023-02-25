from flask import Blueprint
from flask import Flask
from flask_restful import Api
from .resouces.login.LoginRoute import add_login_routes
from .resouces.products.ProductRoute import add_product_routes
from .resouces.StockMovements.StockMovementsRoute import add_stock_routes
bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app: Flask):
    '''Coloca as rotas na aplicação.'''
    add_login_routes(bp, api, app)
    add_product_routes(bp, api, app)
    add_stock_routes(bp, api, app)

    # Registra o blueprint
    app.register_blueprint(bp)
