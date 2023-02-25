from flask import jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required, verify_jwt_in_request, get_jwt_identity
from ...resouces.products.ProductResource import ProductItemResource, ProductResource, ProductPutItemResouce, ProductDeleteItemResouce


def add_product_routes(bp, api, app):
    jwt = JWTManager(app)

    # @app.errorhandler(Exception)
    # def handle_errors(e):
    #     return jsonify({"error": "Internal Server Error"}), 404

    # Define a função de proteção de rota dentro do Blueprint
    @jwt_required
    @bp.route('/product/')
    def protected_view():
        '''Verifica o token passado na rota de produtos.'''
        verify_jwt_in_request()
        products = ProductResource()
        return products.get()

    @jwt_required
    @bp.route('/product/<product_id>')
    def protected_product_item_view(product_id):
        '''Verifica o token passado na rota de um produto específico.'''
        verify_jwt_in_request()
        product = ProductItemResource()
        return product.get(product_id)

    @jwt_required
    @bp.route('/product/', methods=['PUT'])
    def protected_product_item_put():
        '''Verifica o token passado na rota de um produto específico.'''

        verify_jwt_in_request()
        user_id = get_jwt_identity()
        product = ProductPutItemResouce()
        return product.put(user_id)

    @jwt_required
    @bp.route('/product/<product_id>', methods=['DELETE'])
    def protected_product_item_delete(product_id):
        '''Verifica o token passado na rota de um produto específico.'''
        verify_jwt_in_request()
        product = ProductDeleteItemResouce()
        return product.delete(product_id)
