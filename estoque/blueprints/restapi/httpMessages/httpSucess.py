def httpSuccess(message: str, status: int = 200):
    '''Interface de sucesso padrão.'''
    return {"msg": message}, status
