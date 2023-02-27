from flask import jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required, verify_jwt_in_request, get_jwt_identity
from ..StockMovements.StockMovementsResource import StockMovementsResource, StockMovementsPutItem


def add_stock_routes(bp, api, app):
    '''Método que adiciona as rotas de controle de estoque'''
    jwt = JWTManager(app)

    # Define a função de proteção de rota dentro do Blueprint
    @jwt_required
    @bp.route('/stockmovements/<top>')
    def stockview(top):
        '''Verifica o token passado na rota de stockmovements.'''
        verify_jwt_in_request()
        stock = StockMovementsResource()
        return stock.get(top)

    # @jwt_required
    # @bp.route('/product/<product_id>')
    # def protected_product_item_view(product_id):
    #     '''Verifica o token passado na rota de um produto específico.'''
    #     verify_jwt_in_request()
    #     product = ProductItemResource()
    #     return product.get(product_id)

    @jwt_required
    @bp.route('/stockmovements/', methods=['POST'])
    def protected_stockMovement_item_put():
        '''Verifica o token passado na rota de inserção de um stockmovements.'''

        verify_jwt_in_request()
        user_id = get_jwt_identity()
        stock = StockMovementsPutItem()
        return stock.put(user_id)

    # @jwt_required
    # @bp.route('/product/<product_id>', methods=['DELETE'])
    # def protected_product_item_delete(product_id):
    #     '''Verifica o token passado na rota de um produto específico.'''
    #     verify_jwt_in_request()
    #     product = ProductDeleteItemResouce()
    #     return product.delete(product_id)
