from typing import Literal
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ...requests.requestChecker import requestChecker
from flask import jsonify, make_response, request, Response
from estoque.models import User, UserPermission
from ...httpMessages.httpError import httpError
from ...httpMessages.httpSucess import httpSuccess
from estoque.ext.database import db
from flask_restful import Resource
from estoque.models import User
import datetime


class LoginCheckResource(Resource):
    '''Classe de operações com o model login para verificar um login específico.'''

    def post(self) -> Response:
        '''verifica senha e retorna o token de acesso.'''

        data = request.get_json() or {}

        if not data:
            return httpError('Bad Request Error')

        check = requestChecker(data, ["user", "senha"])

        if check != True:
            return check

        username = data.get('user')

        password = data.get('senha')

        user_database = User.query.filter_by(username=username).first()
        # Verifica o usuário e a senha no banco de dados ou em outro sistema de autenticação
        # Substitua essa verificação com seu próprio código de autenticação

        if password is None:
            return httpError('Missing password')

        if not user_database:
            return httpError("User Does not Exist", 404)

        if not check_password_hash(user_database.password, password):
            return httpError("Password is wrong", 401)
        # Cria um token JWT válido por 15 minutos
        access_token = create_access_token(
            identity=user_database.id, expires_delta=datetime.timedelta(minutes=15))

        response = make_response(
            jsonify({'access_token': access_token}), 200)

        return response

    def patch(self, id_user, user_id) -> Response:
        '''verifica senha e retorna o token de acesso.'''
        data = request.get_json() or {}

        check = requestChecker(
            data, ["permissions"])

        if check != True:
            return check

        if not data:
            return httpError('Bad Request Error')

        user_permissions = ['read_users',
                            'create_user', 'update_user', 'delete_user']

        product_permissions = ['read_products',
                               'create_products', 'update_products', 'delete_products']

        product_type_permissions = ['read_product_type',
                                    'create_product_type', 'update_product_type', 'delete_product_type']

        user_permission = UserPermission.query.filter_by(
            user_id=user_id).first()

        if not user_permission:
            return httpError("You have no permissions", 403)

        if user_permission.permission != 'administrador':
            return httpError("You are not an administrator", 403)

        id_user_database = id_user

        user_database = User.query.filter_by(id=id_user_database).first()

        user_database_permissions = UserPermission.query.filter_by(
            user_id=id_user_database).all()

        if not user_database:
            return httpError("User Does not Exist", 404)

        permissions = data.get('permissions')

        if permissions is None:
            return httpError('Missing permissions')

        if "administrador" in permissions:
            # Remover todas as permissões anteriores
            UserPermission.query.filter_by(user_id=id_user_database).delete()

            # Adicionar apenas a permissão de administrador
            user_permission = UserPermission(
                user_id=id_user_database, permission="administrador")
            db.session.add(user_permission)
        else:
            if not set(permissions).issubset(set(user_permissions + product_permissions + product_type_permissions)):
                return httpError("any of your past permissions do not exist", 404)

            # Verificar quais permissões já existem para o usuário
            existing_permissions = [
                p.permission for p in user_database_permissions]

            # Adicionar apenas as permissões que não existem
            for permission in permissions:
                if 'administrador' in existing_permissions:
                    UserPermission.query.filter(
                        UserPermission.user_id == id_user_database, UserPermission.permission == 'administrador').delete()

                if permission not in existing_permissions:
                    user_permission = UserPermission(
                        user_id=id_user_database, permission=permission)
                    db.session.add(user_permission)

        db.session.commit()
        return httpSuccess('Permissions_changed')


class LoginCreateResource(Resource):
    '''Classe de operações com o model login para criação de um.'''

    def post(self) -> Response:
        '''verifica senha e retorna o token de acesso.'''
        data = request.get_json() or {}

        check = requestChecker(data, ["user", "senha", "confirmacao_senha"])

        if check != True:
            return check

        if not data:
            return httpError('Bad Request Error')

        username = data.get('user')

        password = data.get('senha')

        password_confirmation = data.get('confirmacao_senha')

        user_database = User.query.filter_by(username=username).first()

        if password is None:
            return httpError('Password permissions')

        if user_database:
            return httpError("User already exists", 401)

        if password != password_confirmation:
            return httpError("password and password confirmation are not the same", 401)

        # Cria uma instância do modelo User com as informações do novo usuário
        new_user = User(
            username=username,
            password=generate_password_hash(password)
        )

        # Adiciona o novo usuário ao banco de dados
        db.session.add(new_user)
        db.session.commit()

        return httpSuccess("User created successfully")
