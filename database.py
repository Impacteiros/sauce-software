import os
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, Boolean, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib
from datetime import datetime

# Conexão BD
db_path = os.path.join(os.getcwd(), 'database.db')
engine = create_engine(f'sqlite:///{db_path}', echo=True)

Base = declarative_base()

class Funcionario(Base):
      __tablename__ = "funcionario"

      id = Column(Integer, primary_key=True)
      nome = Column(String(100))
      usuario = Column(String(20))
      senha = Column(String(20))
      cargo = Column(String(20))

class Produto(Base):
      __tablename__ = "produto"

      id = Column(Integer, primary_key=True)
      nome = Column(String(20))
      preco = Column(Numeric(precision=5, scale=2))
      descricao = Column(String(100))
      url_imagem = Column(String)
      categoria = Column(String(20))
      ativo = Column(Boolean)

class Pedido(Base):
      __tablename__ = "pedido"

      id = Column(Integer, primary_key=True)
      id_cliente = Column(Integer)
      ids_lanches = Column(String(100))
      total = Column(Numeric(precision=5, scale=2))
      data = Column(DateTime)
      atendente = Column(String(20))
      mesa = Column(Integer)

class Cliente(Base):
      __tablename__ = "cliente"

      id = Column(Integer, primary_key=True)
      nome = Column(String(50))
      endereco = Column(String(200))
      celular = Column(String(15))
      email = Column(String(50))

# Criando a tabela no banco de dados
Base.metadata.create_all(engine)

# Criando uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

def cadastrar_funcionario(nome, usuario, senha, cargo):
      engine.connect()
      senha_hash = hashlib.sha256(senha.encode()).hexdigest()
      funcionario = Funcionario(nome=nome, usuario=usuario, senha=senha_hash, cargo=cargo)
      session.add(funcionario)
      session.commit()
      session.close()

def validar_login(usuario, senha):
      engine.connect()
      resp_usuario = session.query(Funcionario).filter(Funcionario.usuario == usuario).first()
      session.close()
      if resp_usuario:
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            if resp_usuario.senha == senha_hash:
                  return [True, resp_usuario.nome, resp_usuario.cargo]
            else:
                  return [False, "Usuário e/ou senha incorreto(s)."]
      return [False, "Usuário e/ou senha incorreto(s)."]


def adicionar_produto(nome, descricao, preco, categoria, url_imagem):
      engine.connect()
      produto = Produto(nome=nome, descricao=descricao, preco=preco, categoria=categoria, url_imagem=url_imagem, ativo=True)
      session.add(produto)
      session.commit()
      session.close()
      
def remover_produto(id):
        engine.connect()
        resultado = session.query(Produto).get(id)
        resultado.ativo = False
        session.commit()
        session.close()

def salvar_pedido(data, id_cliente, usuario, preco, mesa):
      engine.connect()
      pedido = Pedido(ids_lanches=data, id_cliente=id_cliente, total=preco, atendente=usuario, data=datetime.now(), mesa=mesa)
      session.add(pedido)
      session.commit()
      session.close()

def cadastrar_cliente(nome, endereco, celular, email):
      engine.connect()
      cliente = Cliente(nome=nome, endereco=endereco, celular=celular, email=email)
      session.add(cliente)
      session.commit()
      session.close()

def pesquisa_cliente(nome):
      engine.connect()
      query = session.query(Cliente).filter(Cliente.nome.like(f'{nome}%')).all()
      session.close()
      return query

def get_cliente(id):
      engine.connect()
      query = session.query(Cliente).get(id)
      session.close()
      return query

def get_produto(id):
      engine.connect()
      session.close()
      return session.query(Produto).get(id)

def editar_produto(id, nome, descricao, preco, categoria, url_imagem):
      engine.connect()
      query = session.query(Produto).get(id)
      query.nome = nome
      query.descricao = descricao
      query.preco = preco
      query.categoria = categoria
      query.url_imagem = url_imagem
      session.commit()

lista_lanches = session.query(Produto).filter(and_(Produto.ativo == True, Produto.categoria == 'hamburguer'))
lista_bebidas = session.query(Produto).filter(and_(Produto.ativo == True, Produto.categoria == 'bebida'))