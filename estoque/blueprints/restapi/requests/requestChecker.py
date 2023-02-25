from estoque.blueprints.restapi.httpMessages.httpError import httpError


def requestChecker(keys, required_keys, required_types=None):
    '''Checa se o corpo da requisição possui as chaves e tipos corretos.'''
    if set(keys) != set(required_keys):
        error_msg = f"Invalid request. Must contain the keys {required_keys}."
        return httpError(error_msg, 400)

    if required_types is not None:
        for key, value in required_types.items():
            if key in keys and value is not None and not isinstance(keys[key], value):
                return httpError(f"Invalid request. '{key}' must be of type {value.__name__}.", 400)

    return True
