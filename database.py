import os
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib
from datetime import datetime

# Conexão BD
db_path = os.path.join(os.getcwd(), 'database.db')
engine = create_engine(f'sqlite:///{db_path}', echo=True)

Base = declarative_base()

class Funcionario(Base):
      __tablename__ = "funcionarios"

      id = Column(Integer, primary_key=True)
      nome = Column(String(100))
      usuario = Column(String(20))
      senha = Column(String(20))
      cargo = Column(String(20))

class Produto(Base):
      __tablename__ = "produtos"

      id = Column(Integer, primary_key=True)
      nome = Column(String(20))
      preco = Column(Numeric(precision=5, scale=2))
      descricao = Column(String(100))
      url_imagem = Column(String)
      ativo = Column(Boolean)

class Pedidos(Base):
      __tablename__ = "pedidos"

      id = Column(Integer, primary_key=True)
      ids_lanches = Column(String(100))
      total = Column(Numeric(precision=5, scale=2))
      data = Column(DateTime)
      atendente = Column(String(20))
      mesa = Column(Integer)

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


def adicionar_produto(nome, descricao, preco, url_imagem):
      engine.connect()
      produto = Produto(nome=nome, descricao=descricao, preco=preco, url_imagem=url_imagem, ativo=True)
      session.add(produto)
      session.commit()
      session.close()
      
def remover_lanche(id):
        engine.connect()
        resultado = session.query(Produto).get(id)
        resultado.ativo = False
        session.commit()
        session.close()

def salvar_pedido(data, usuario, preco, mesa):
      engine.connect()
      pedido = Pedidos(ids_lanches=data, total=preco, atendente=usuario, data=datetime.now(), mesa=mesa)
      session.add(pedido)
      session.commit()
      session.close()

def get_lanche(id):
      return session.query(Produto).get(id)

lista_lanches = session.query(Produto).filter(Produto.ativo == True)
