from enum import Enum


class TipoMovimentacao(Enum):
    '''Enum que define o tipo de movimenção como entrada e saída.'''
    ENTRADA = "entrada"
    SAIDA = "saida"
