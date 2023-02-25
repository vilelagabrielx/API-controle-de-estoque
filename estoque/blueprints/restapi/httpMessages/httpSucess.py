def httpSuccess(message: str, status: int = 200):
    '''Interface de erro padrão.'''
    return {"msg": message}, status
