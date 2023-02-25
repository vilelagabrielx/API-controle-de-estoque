from flask import jsonify, request
from estoque.blueprints.restapi.httpMessages.httpSucess import httpSuccess
from estoque.blueprints.restapi.httpMessages.httpError import httpError
from estoque.blueprints.restapi.requests.requestChecker import requestChecker
from estoque.models import Product
from flask_restful import Resource
from ...httpMessages.httpError import httpError
from estoque.ext.database import db


class ProductResource(Resource):
    '''Classe de operações com o model produto para todos os produtos.'''

    def get(self):
        '''Retorna todos os produtos'''
        products = Product.query.all()
        return jsonify(
            {"products": [product.to_dict() for product in products]}
        )


class ProductItemResource(Resource):
    '''Classe de operações com o model produto para um produto específico.'''

    def get(self, product_id):
        '''Retorna um produto específico'''
        product = Product.query.filter_by(id=product_id).first()
        if product:
            return jsonify(product.to_dict())
        else:
            return httpError("Product does not exist", 404)


class ProductDeleteItemResouce(Resource):
    def delete(self, product_id):
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return httpError('Product does not exist', 404)
        db.session.delete(product)
        db.session.commit()
        return httpSuccess('Product deleted successfully')


class ProductPutItemResouce(Resource):
    def put(self, user_id):
        data = request.get_json() or {}

        check = requestChecker(data, ["nome", "quantidade", "preco"])

        if check != True:
            return check
        nome = request.json.get("nome")
        quantidade = request.json.get("quantidade")
        preco = request.json.get("preco")
        product = Product.query.filter_by(nome=nome).first()
        if product:
            return httpError('The database already has a product registered with this name')

        new_product = Product(
            nome=nome,
            quantidade=quantidade,
            preco=preco,
            create_user=int(user_id)
        )
        db.session.add(new_product)
        db.session.commit()
        return httpSuccess('Product created successfully')
