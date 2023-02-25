from importlib import import_module

from dynaconf import FlaskDynaconf
from flask import Flask


def load_extensions(app: Flask) -> Flask:
    '''Carrega as extensões definidas no settings.toml e importa elas.'''
    # Itera sobre todas as extensões definidas na configuração da aplicação.
    for extension in app.config.EXTENSIONS:
        # Divide a string da extensão em duas partes, separadas pelo caractere ':'.
        # A primeira parte é o nome do módulo Python que implementa a extensão.
        # A segunda parte é o nome da função factory que será invocada para inicializar a extensão.
        module_name, factory = extension.split(":")
        # Importa dinamicamente o módulo da extensão.
        ext = import_module(module_name)
        # Invoca a função factory passando o objeto Flask como argumento.
        getattr(ext, factory)(app)
        # Sobre a função factory
        # Em Python, uma função factory é uma função que retorna outra função
        # ou objeto. No contexto de extensões do Flask, a função factory é
        # responsável por criar e inicializar a extensão, e retornar um objeto
        # que será associado à sua aplicação Flask.
        # A linha de código getattr(ext, factory)(app) invoca a função factory
        # da extensão dinamicamente, passando o objeto Flask app como argumento.
        # O uso da função getattr permite obter a referência da função factory a
        # partir do nome da função armazenado na variável factory.
        # Por exemplo, se a extensão definida na configuração da aplicação
        # for flask_bootstrap: Bootstrap, o código irá importar o módulo flask_bootstrap e
        # invocar a função Bootstrap desse módulo, passando o objeto app como argumento. A função Bootstrap é a função factory que retorna um objeto Bootstrap que será associado à sua aplicação Flask.
        # Assim, as funções factory permitem que as extensões possam ser criadas de forma flexível e configurável, permitindo que você customize a inicialização de cada extensão de acordo com as necessidades da sua aplicação.


def init_app(app: Flask, **config) -> Flask:
    '''Manda o app para a classe de configurações. As configurações são feitas
    no arquivo settings.toml.'''
    FlaskDynaconf(app, **config)
