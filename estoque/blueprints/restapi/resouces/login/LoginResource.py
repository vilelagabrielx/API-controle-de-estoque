from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from ...requests.requestChecker import requestChecker
from flask import abort, jsonify, request
from estoque.models import User
from ...httpMessages.httpError import httpError
from ...httpMessages.httpSucess import httpSuccess
from estoque.ext.database import db
from flask_restful import Resource
from estoque.models import User
import datetime


class LoginCheckResource(Resource):
    '''Classe de operações com o model login para verificar um login específico.'''

    def post(self):
        '''verifica senha e retorna o token de acesso.'''
        username = request.json.get("user")

        password = request.json.get("senha")

        data = request.get_json() or {}

        check = requestChecker(data, ["user", "senha"])

        if check != True:
            return check

        user_database = User.query.filter_by(username=username).first()
        # Verifica o usuário e a senha no banco de dados ou em outro sistema de autenticação
        # Substitua essa verificação com seu próprio código de autenticação
        if not user_database:
            return httpError("User Does not Exist", 404)

        if not check_password_hash(user_database.password, password):
            return httpError("Password is wrong", 401)
        # Cria um token JWT válido por 15 minutos
        access_token = create_access_token(
            identity=user_database.id, expires_delta=datetime.timedelta(minutes=15))

        return {"access_token": access_token}, 200


class LoginCreateResource(Resource):
    '''Classe de operações com o model login para criação de um.'''

    def post(self):
        '''verifica senha e retorna o token de acesso.'''
        data = request.get_json() or {}

        check = requestChecker(data, ["user", "senha", "confirmacao_senha"])

        if check != True:
            return check

        username = request.json.get("user")
        password = request.json.get("senha")
        password_confirmation = request.json.get("confirmacao_senha")
        user_database = User.query.filter_by(username=username).first()
        print(user_database)
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
