from flask import jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required, verify_jwt_in_request, get_jwt_identity
from ...resouces.ProductType.ProductTypeResource import ProductTypeResource, ProducttypePutItemResouce, ProductTypeItemResource


def add_product_type_routes(bp, api, app):
    jwt = JWTManager(app)

    # Define a função de proteção de rota dentro do Blueprint

    @jwt_required
    @bp.route('/producttype/')
    def protected_view_product_type():
        '''Verifica o token passado na rota de produtos.'''
        verify_jwt_in_request()
        productstype = ProductTypeResource()
        return productstype.get()

    @jwt_required
    @bp.route('/producttype/<producttype_id>')
    def protected_product_type_item_view(producttype_id):
        '''Verifica o token passado na rota de um produto específico.'''
        verify_jwt_in_request()
        product = ProductTypeItemResource()
        return product.get(producttype_id)

    @jwt_required
    @bp.route('/producttype/', methods=['PUT'])
    def protected_product_type_item_put():
        '''Verifica o token passado na rota de um produto específico.'''

        verify_jwt_in_request()
        user_id = get_jwt_identity()
        producttype = ProducttypePutItemResouce()
        return producttype.put(user_id)

    # @jwt_required
    # @bp.route('/producttype/<producttype_id>', methods=['DELETE'])
    # def protected_product_item_delete(product_id):
    #     '''Verifica o token passado na rota de um produto específico.'''
    #     verify_jwt_in_request()
    #     product = ProductItemResource()
    #     return product.delete(product_id)
