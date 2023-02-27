from flask import make_response, jsonify,Response


def httpError(message: str, status: int = 400) -> Response:
    '''Interface de erro padrão.'''
    response = make_response(jsonify({'msg': message}), status)
    response.headers['Content-Type'] = 'application/json'
    return response
