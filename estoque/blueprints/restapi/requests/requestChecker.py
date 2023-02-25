from estoque.blueprints.restapi.httpMessages.httpError import httpError


def requestChecker(keys, required_keys, required_types=None):
    '''
    Verifica se a requisição contém as chaves e tipos corretos.

    Args:
        keys (dict): Dicionário com as chaves da requisição.
        required_keys (list): Lista com as chaves requeridas pela API.
        required_types (dict, optional): Dicionário com as chaves e tipos requeridos pela API. Defaults to None.

    Returns:
        bool or Response: Retorna True se a requisição é válida, caso contrário retorna um objeto Response com mensagem de erro.
    '''
    # Verifica se as chaves presentes na requisição são as requeridas pela API
    if set(keys) != set(required_keys):
        error_msg = f"Invalid request. Must contain the keys {required_keys}."
        return httpError(error_msg, 400)

    # Verifica se os valores presentes nas chaves da requisição são do tipo correto
    if required_types is not None:
        for key, value in required_types.items():
            if key in keys and value is not None and not isinstance(keys[key], value):
                return httpError(f"Invalid request. '{key}' must be of type {value.__name__}.", 400)

    # Retorna True se a requisição é válida
    return True
