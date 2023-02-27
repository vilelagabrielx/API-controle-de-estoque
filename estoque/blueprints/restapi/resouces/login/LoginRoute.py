from flask import jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required, verify_jwt_in_request, get_jwt_identity
from ...resouces.login.LoginResource import LoginCheckResource, LoginCreateResource


def add_login_routes(bp, api, app):
    jwt = JWTManager(app)

    @jwt_required
    @bp.route('/login/permission/<user_change>', methods=['PATCH'])
    def protected_update_permissions_user(user_change):
        '''Verifica o token passado na rota de um tipo de produto específico.'''
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        permission = LoginCheckResource()
        return permission.patch(user_change, user_id)
    api.add_resource(LoginCheckResource, "/login", methods=['POST'])
    api.add_resource(LoginCreateResource, "/login/create", methods=['POST'])
