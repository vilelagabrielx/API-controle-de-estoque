from flask import Flask

from estoque.ext import configuration
# A APLICAÇÃO É FEITA UTILIZANDO FACTORY PATTERN + BLUE PRINT
# PRIMEIRAMENTE É FEITA UMA CRIAÇÃO DO APP NA FORMA MAIS SIMPLES
# DEPOIS É PRA IR IMPLEMENTANDO ELA COM MAIS COISAS


def minimal_app(**config) -> Flask:
    # AQUI O APP DO FLASK É IMPLEMENTADO DE FORMA SIMPLES(LINHA 11)
    '''Inicia um app flask com as configurações mínimas'''
    app = Flask(__name__)
    configuration.init_app(app, **config)
    return app
#### O CREATE APP É EXECUTADO PRIMEIRO##############
# VISTO QUE NO ARQUIVO .ENV ESTÁ DEFINIDO QUE O FLASK_APP É ELE


def create_app(**config) -> Flask:  # o **config são os parametros passados para o flask run
    '''Inicia um app no flask com as configurações passadas.'''
    app = minimal_app(
        **config)  # RESPEITANDO A ARQUITETURA VIGENTE INICIA O FLASK
    configuration.load_extensions(app)  # carrega extensões,
    # (ou modulos pra fazer coisas)
    # os modulos estão em settings.toml em EXTENSIONS
    return app
