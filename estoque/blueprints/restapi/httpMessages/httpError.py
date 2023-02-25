def httpError(message: str, status: int = 400):
    '''Interface de erro padrão.'''
    return {"msg": message}, status
