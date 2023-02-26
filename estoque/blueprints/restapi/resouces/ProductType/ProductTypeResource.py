from flask import jsonify, request
from estoque.blueprints.restapi.httpMessages.httpSucess import httpSuccess
from estoque.blueprints.restapi.httpMessages.httpError import httpError
from estoque.blueprints.restapi.requests.requestChecker import requestChecker
from estoque.models import ProductTypes
from flask_restful import Resource
from ...httpMessages.httpError import httpError
from estoque.ext.database import db


class ProductTypeResource(Resource):
    '''Classe de operações com o model do tipo de produto para todos os tipos.'''

    def get(self):
        '''Retorna todos os tipos de produtos'''
        productstypes = ProductTypes.query.all()
        return jsonify(
            {"tipos": [producttype.to_dict()
                       for producttype in productstypes]}
        )


class ProductTypeItemResource(Resource):
    '''Classe de operações com o model do tipo de produto para um produto específico.'''

    def get(self, producttype_id):
        '''Retorna um produto específico'''
        productstypes = ProductTypes.query.filter_by(ID=producttype_id).first()
        if productstypes:
            return jsonify(productstypes.to_dict())
        else:
            return httpError("Product type does not exist", 404)

    def delete(self, producttype_id):
        productstypes = ProductTypes.query.filter_by(ID=producttype_id).first()
        if not productstypes:
            return httpError('Product type does not exist', 404)
        db.session.delete(productstypes)
        db.session.commit()
        return httpSuccess('Product type deleted successfully')

    def put(self, producttype_id):
        productstypes = ProductTypes.query.filter_by(ID=producttype_id).first()

        if not productstypes:
            return httpError('Product type does not exist', 404)

        data = request.get_json() or {}

        check = requestChecker(
            data, ["nome"])

        if check != True:
            return check
        nome = request.json.get("nome")

        productstypes.nome = nome

        db.session.commit()

        return httpSuccess('Product type updated successfully')


class ProducttypeCREATEItemResouce(Resource):
    def post(self, user_id):
        data = request.get_json() or {}

        check = requestChecker(
            data, ["nome"])

        if check != True:
            return check
        nome = request.json.get("nome")
        product = ProductTypes.query.filter_by(nome=nome).first()
        if product:
            return httpError('The database already has a product type registered with this name')

        new_producttype = ProductTypes(
            nome=nome
        )
        db.session.add(new_producttype)
        db.session.commit()
        return httpSuccess('Product type created successfully')
