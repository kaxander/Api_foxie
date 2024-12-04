#importar bibliotecas
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Enum, Float
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, declarative_base
from enum import Enum as PyEnum
from datetime import datetime

#configurar banco
engine = create_engine('postgresql://postgres.wyekqwsnuvyrjpdvmxkl:galuma729863@aws-0-sa-east-1.pooler.supabase.com:6543/postgres')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)
    email = Column(String(40), nullable=False, unique=True)
    senha = Column(String(40), nullable=False)
    cpf = Column(String(40), nullable=False, unique=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def serialize(self):
        dados_admin = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'cpf': self.cpf,
        }
        return dados_admin

class Categoria(Base):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)
    icone = Column(String(5))
    admin_id = Column(Integer, ForeignKey('admin.id'))

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        dados_categoria = {
            'id': self.id,
            'nome': self.nome,
            'icone': self.icone,
            'admin_id': self.admin_id,
        }
        return dados_categoria

class Funcionario(Base):
    __tablename__ = 'funcionario'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)
    email = Column(String(40), nullable=False, unique=True)
    senha = Column(String(40), nullable=False)
    telefone = Column(String(40), nullable=False, unique=True)
    admin_id = Column(Integer, ForeignKey('admin.id'))

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        dados_funcionario = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'telefone': self.telefone,
            'admin_id': self.admin_id,
        }
        return dados_funcionario

class Produto(Base):
    __tablename__ = 'produto'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False)
    descricao = Column(String(40), nullable=False)
    imagem = Column(String(40), nullable=False)
    preco = Column(Float, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categoria.id'))

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        dados_produto = {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'imagem': self.imagem,
            'preco': self.preco,
            'categoria_id': self.categoria_id,
        }
        return dados_produto

# class Ingrediente(Base):
#     __tablename__ = 'ingrediente'
#     id = Column(Integer, primary_key=True)
#     nome = Column(String(40), nullable=False)
#     produto_id = Column(Integer, ForeignKey('produto.id'))
#
#     def save(self):
#         db_session.add(self)
#         db_session.commit()
#
#     def delete(self):
#         db_session.delete(self)
#         db_session.commit()
#
#     def serialize(self):
#         dados_ingrediente = {
#             'id': self.id,
#             'nome': self.nome,
#             'produto_id': self.produto_id,
#         }
#         return dados_ingrediente

# Definição do Enum Python para o status
class StatusPedido(PyEnum):
    PENDENTE = "PENDENTE"
    EM_ESPERA = "EM_ESPERA"
    EM_PRODUCAO = "EM_PRODUCAO"
    FINALIZADO = "FINALIZADO"

class Pedido(Base):
    __tablename__ = 'pedido'
    id = Column(Integer, primary_key=True)
    mesa = Column(String(10), nullable=False)
    status = Column(Enum(StatusPedido), nullable=False, default=StatusPedido.EM_ESPERA)
    dataCriado = Column(DateTime)
    funcionario_id = Column(Integer, ForeignKey('funcionario.id'))
    relationship(Funcionario)

    def save(self):
        if not self.dataCriado:
            self.dataCriado = datetime.now()
        db_session.add(self)
        db_session.commit()

    def serialize(self):
        dados_pedido = {
            'id': self.id,
            'mesa': self.mesa,
            'status': self.status.value,
            'dataCriado': self.dataCriado.strftime("%d/%m/%Y %H:%M:%S") if self.dataCriado else None,
            'funcionario_id': self.funcionario_id
        }
        return dados_pedido


class PedidoProduto(Base):
    __tablename__ = 'pedidoproduto'
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produto.id'))
    relationship(Produto)
    pedido_id = Column(Integer, ForeignKey('pedido.id'))
    relationship(Pedido)
    quantidade = Column(Integer, nullable=False, default=1)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize(self):
        dados_pedidoProduto = {
            'id': self.id,
            'produto_id': self.produto_id,
            'pedido_id': self.pedido_id,
            'quantidade': self.quantidade,
        }
        return dados_pedidoProduto

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)