from flask import jsonify, request
from estoque.blueprints.restapi.httpMessages.httpSucess import httpSuccess
from estoque.blueprints.restapi.httpMessages.httpError import httpError
from estoque.blueprints.restapi.requests.requestChecker import requestChecker
from estoque.models import ProductTypes, UserPermission
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
            return httpError("Product type does not exist", 403)

    def delete(self, producttype_id, user_id):
        user_permission = UserPermission.query.filter_by(
            user_id=user_id).first()

        if not user_permission:
            return httpError("You have no permissions", 403)

        if user_permission.permission not in ['delete_user_type', 'administrador']:
            return httpError("You don't have permission to delete a product type", 403)

        productstypes = ProductTypes.query.filter_by(ID=producttype_id).first()

        if not productstypes:
            return httpError('Product type does not exist', 404)

        db.session.delete(productstypes)

        db.session.commit()

        return httpSuccess('Product type deleted successfully')

    def put(self, producttype_id, user_id):
        productstypes = ProductTypes.query.filter_by(ID=producttype_id).first()

        user_permission = UserPermission.query.filter_by(
            user_id=user_id).first()

        if not user_permission:
            return httpError("You have no permissions", 403)

        if user_permission.permission not in ['update_user_type', 'administrador']:
            return httpError("You don't have permission to update a product type", 403)

        if not productstypes:
            return httpError('Product type does not exist', 404)

        data = request.get_json() or {}

        if not data:
            return httpError('Bad Request Error')

        check = requestChecker(
            data, ["nome"])

        if check != True:
            return check
        nome = data.get('nome')

        productstypes.nome = nome

        db.session.commit()

        return httpSuccess('Product type updated successfully')


class ProducttypeCREATEItemResouce(Resource):
    def post(self, user_id):

        user_permission = UserPermission.query.filter_by(
            user_id=user_id).first()

        if not user_permission:
            return httpError("You have no permissions", 403)

        if user_permission.permission not in ['create_product_type', 'administrador']:
            return httpError("You don't have permission to create a product type", 403)

        data = request.get_json() or {}

        if not data:
            return httpError('Bad Request Error')

        check = requestChecker(
            data, ["nome"])

        if check != True:
            return check

        nome = data.get('nome')

        product = ProductTypes.query.filter_by(nome=nome).first()

        if product:
            return httpError('The database already has a product type registered with this name')

        new_producttype = ProductTypes(
            nome=nome
        )

        db.session.add(new_producttype)

        db.session.commit()

        return httpSuccess('Product type created successfully')
