from datetime import datetime
import pytz
from estoque.ext.database import db
from sqlalchemy_serializer import SerializerMixin
timezone = pytz.timezone('America/Sao_Paulo')


class ProductTypes(db.Model, SerializerMixin):
    __tablename__ = 'tipoProduto'
    '''Modelo da tabela user, tabela onde os logins são armazenados.'''
    ID = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(500))


class Product(db.Model, SerializerMixin):
    __tablename__ = 'product'
    '''Modelo da tabela product, para os produtos do estoque.'''
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(140))
    quantidade = db.Column(db.Numeric())
    preco = db.Column(db.Numeric(100, 2))
    create_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone))
    idtipo = db.Column(db.Integer, db.ForeignKey('tipoProduto.ID'))


class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    '''Modelo da tabela user, tabela onde os logins são armazenados.'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))


class StockMovements(db.Model, SerializerMixin):
    __tablename__ = 'StockMovements'
    '''Modelo da tabela StockMovements, tabela onde as movimentações de estoque são armazenadas.'''
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum('entrada', 'saida'))
    quantidade = db.Column(db.Numeric())
    data = db.Column(db.DateTime, default=datetime.now(timezone))
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    produto_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantidade_antiga_produtos = db.Column(db.Numeric())
    quantidade_atual_produtos = db.Column(db.Numeric())
