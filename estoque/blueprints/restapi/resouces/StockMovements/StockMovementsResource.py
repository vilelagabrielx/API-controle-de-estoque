from flask import jsonify, request
from estoque.blueprints.restapi.httpMessages.httpSucess import httpSuccess
from estoque.blueprints.restapi.httpMessages.httpError import httpError
from estoque.blueprints.restapi.requests.requestChecker import requestChecker
from estoque.models import Product, StockMovements, User
from flask_restful import Resource
from ...httpMessages.httpError import httpError
from estoque.ext.database import db
from datetime import datetime
from enum import Enum
import pytz
timezone = pytz.timezone('America/Sao_Paulo')


class StockMovementsResource(Resource):
    '''Classe de operações com o model de movimentação de estoque(todas as movimentações).'''

    def get(self, top):
        '''Retorna todos os movimentos de estoque'''

        stock = StockMovements.query.order_by(
            StockMovements.data.desc()).limit(top).all()
        if not stock:
            return httpError("There's no a Stock Movement on database", 404)
        return jsonify(
            {"stock movements": [item.to_dict() for item in stock]}
        )


class StockMovementsByID(Resource):
    '''Classe de operações com o model de movimentação de estoque para um id de operação específico.'''

    def get(self, stock_id):
        '''Retorna um movimento de estoque específico'''
        StockMovements = StockMovements.query.filter_by(id=stock_id).first()
        if StockMovements:
            return jsonify(StockMovements.to_dict())
        else:
            return httpError("There's no a Stock Movement with this id", 404)


class StockMovementsByUserID(Resource):
    '''Classe de operações com o model de movimento de estoque de um usuário específico.'''

    def get(self, user_id):
        '''Retorna um movimento de estoque de um usuário específico.'''
        user_database = User.query.filter_by(id=user_id).first()

        if not user_database:
            return httpError("User Does not Exist", 404)

        StockMovements = StockMovements.query.filter_by(
            usuario_id=user_id).all()

        return jsonify(
            {"stock movements": [item.to_dict() for item in StockMovements]}
        )


class StockMovementsByProductID(Resource):
    '''Classe de operações com o model de movimento de estoque de um produto específico.'''

    def get(self, product_id):
        '''Retorna um movimento de estoque de um produto específico.'''
        product_database = User.query.filter_by(produto_id=product_id).first()

        if not product_database:
            return httpError('Product does not exist', 404)

        StockMovements = StockMovements.query.filter_by(
            produto_id=product_id).all()

        return jsonify(
            {"stock movements": [item.to_dict() for item in StockMovements]}
        )

# class ProductDeleteItemResouce(Resource):
#     def delete(self, product_id):
#         product = Product.query.filter_by(id=product_id).first()
#         if not product:
#             return httpError('Product does not exist', 404)
#         db.session.delete(product)
#         db.session.commit()
#         return httpSuccess('Product deleted successfully')


class TipoMovimentacao(Enum):
    '''Enum que define o tipo de movimenção como entrada e saída.'''
    ENTRADA = "entrada"
    SAIDA = "saida"


class StockMovementsPutItem(Resource):
    '''Classe de insert do banco de dados de um movimento de estoque.'''

    def put(self, user_id):
        '''Insere um movimento de estoque.'''
        data = request.get_json() or {}

        # Verificar se a solicitação tem os campos obrigatórios e seus tipos estão corretos.
        required_keys = ["tipo", "quantidade", "produto_id"]
        required_types = {
            "tipo": str,
            "quantidade": int,
            "produto_id": int
        }
        check = requestChecker(data, required_keys, required_types)
        if check != True:
            return check

        try:
            tipo = TipoMovimentacao(request.json["tipo"])
        except:
            return httpError(
                f"Invalid request. 'tipo' must be 'entrada' or 'saida'.", 400)

        quantidade = request.json["quantidade"]

        produto_id = request.json["produto_id"]

        # Verificar se o produto existe
        product = Product.query.filter_by(id=produto_id).first()

        if not product:
            return httpError('Product does not exist', 404)

        # Calcular a nova quantidade do produto
        if tipo == TipoMovimentacao.ENTRADA:
            new_quantity = quantidade + product.quantidade
        else:  # tipo == TipoMovimentacao.SAIDA
            new_quantity = quantidade - product.quantidade
            if new_quantity < 0:
                return httpError('Not enough products', 404)

        new_StockMovement = StockMovements(
            tipo=tipo.value,
            quantidade=quantidade,
            usuario_id=user_id,
            produto_id=produto_id,
            quantidade_antiga_produtos=product.quantidade,
            quantidade_atual_produtos=new_quantity
        )
        product.quantidade = new_quantity
        product.updated_at = datetime.now(timezone)

        # Registrar a nova movimentação de estoque no banco de dados

        db.session.add(new_StockMovement)
        db.session.commit()

        # Retornar uma resposta de sucesso
        return httpSuccess('The stock movement has been recorded')
