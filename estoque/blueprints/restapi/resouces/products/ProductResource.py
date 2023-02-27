from flask import jsonify, request, Response
from estoque.blueprints.restapi.httpMessages.httpSucess import httpSuccess
from estoque.blueprints.restapi.httpMessages.httpError import httpError
from estoque.blueprints.restapi.requests.requestChecker import requestChecker
from estoque.models import Product, ProductTypes
from flask_restful import Resource
from ...httpMessages.httpError import httpError
from estoque.ext.database import db


class ProductResource(Resource):
    '''Classe de operações com o model produto para todos os produtos.'''

    def get(self) -> Response:
        '''Retorna todos os produtos'''
        products = Product.query.all()
        return jsonify(
            {"products": [product.to_dict() for product in products]}
        )


class ProductItemResource(Resource):
    '''Classe de operações com o model produto para um produto específico.'''

    def get(self, product_id) -> Response:
        '''Retorna um produto específico'''
        product = Product.query.filter_by(id=product_id).first()
        if product:
            return jsonify(product.to_dict())
        else:
            return httpError("Product does not exist", 404)

    def delete(self, product_id) -> Response:
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return httpError('Product does not exist', 404)
        db.session.delete(product)
        db.session.commit()
        return httpSuccess('Product deleted successfully')


class ProductCREATEItemResouce(Resource):
    def post(self, user_id) -> Response:
        data = request.get_json() or {}

        if not data:
            return httpError('Bad Request Error')

        check = requestChecker(
            data, ["nome", "quantidade", "preco", "tipoProduto"])

        if check != True:
            return check

        nome = data.get('nome')

        quantidade = data.get('quantidade')

        preco = data.get('preco')

        tipo_produto = data.get('tipoProduto')

        product = Product.query.filter_by(nome=nome).first()

        if product:
            return httpError('The database already has a product registered with this name')

        tipoProduto = ProductTypes.query.filter_by(nome=tipo_produto).first()

        if not tipoProduto:
            return httpError('Product type does not exist')

        new_product = Product(
            nome=nome,
            quantidade=quantidade,
            preco=preco,
            create_user=int(user_id),
            idtipo=tipoProduto.ID
        )
        db.session.add(new_product)
        db.session.commit()
        return httpSuccess('Product created successfully')
