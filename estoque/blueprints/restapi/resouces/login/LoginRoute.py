from flask import jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required, verify_jwt_in_request, get_jwt_identity
from ...resouces.login.LoginResource import LoginCheckResource, LoginPutResource


def add_login_routes(bp, api, app):
    jwt = JWTManager(app)

    # @app.errorhandler(Exception)
    # def handle_errors(e):
    #     return jsonify({"error": "Internal Server Error"}), 404

    api.add_resource(LoginCheckResource, "/login")
    api.add_resource(LoginPutResource, "/login/create")
