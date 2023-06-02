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
      ativo = Column(Boolean)

class Produto(Base):
      __tablename__ = "produto"

      id = Column(Integer, primary_key=True)
      nome = Column(String(20))
      preco = Column(Numeric(precision=5, scale=2))
      descricao = Column(String(100))
      url_imagem = Column(String)
      categoria = Column(String(20))
      ativo = Column(Boolean)
      disponivel = Column(Boolean)

class Pedido(Base):
      __tablename__ = "pedido"

      id = Column(Integer, primary_key=True)
      id_cliente = Column(Integer)
      ids_lanches = Column(String(100))
      total = Column(Numeric(precision=5, scale=2))
      data = Column(DateTime)
      atendente = Column(String(20))
      cupom = Column(String(22))
      mesa = Column(Integer)

class Cliente(Base):
      __tablename__ = "cliente"

      id = Column(Integer, primary_key=True)
      nome = Column(String(50))
      endereco = Column(String(200))
      celular = Column(String(15))
      email = Column(String(50))

class Adicional(Base):
      __tablename__ = "adicional"

      id = Column(Integer, primary_key=True)
      nome = Column(String(50))
      preco = Column(Numeric(precision=5, scale=2))
      url_imagem = Column(String)
      disponivel = Column(Boolean)
      ativo = Column(Boolean)

class Cupom(Base):
      __tablename__ = "cupom"

      id = Column(Integer, primary_key=True)
      cupom = Column(String(20))
      valor = Column(Numeric(precision=5, scale=2))
      ativo = Column(Boolean)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def cadastrar_funcionario(nome, usuario, senha, cargo):
      engine.connect()
      senha_hash = hashlib.sha256(senha.encode()).hexdigest()
      funcionario = Funcionario(nome=nome, usuario=usuario, senha=senha_hash, cargo=cargo, ativo=True)
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

def validar_cupom(cupom_desejado):
      engine.connect()
      query = session.query(Cupom).filter(Cupom.cupom == cupom_desejado).first()
      return query

def cadastrar_cupom(cupom, valor):
      engine.connect()
      cupom = Cupom(cupom=cupom, valor=valor, ativo=True)
      session.add(cupom)
      session.commit()
      session.close()

def deletar_cupom(id):
      engine.connect()
      cupom = session.query(Cupom).get(id)
      cupom.ativo = False
      session.commit()
      session.close()

def validar_cadastro(usuario):
      query = session.query(Funcionario).filter(Funcionario.usuario == usuario).first()
      if query:
            return True
      return False

def adicionar_produto(nome, descricao, preco, categoria, url_imagem):
      engine.connect()
      produto = Produto(nome=nome, descricao=descricao, preco=preco, categoria=categoria, url_imagem=url_imagem, ativo=True, disponivel=True)
      session.add(produto)
      session.commit()
      session.close()

def adicionar_adicional(nome, preco, url_imagem):
      engine.connect()
      produto = Adicional(nome=nome, preco=preco, url_imagem=url_imagem, ativo=True, disponivel=True)
      session.add(produto)
      session.commit()
      session.close()
      
      
def remover_produto(id):
        engine.connect()
        resultado = session.query(Produto).get(id)
        resultado.ativo = False
        session.commit()
        session.close()

def remover_funcionario(id):
        engine.connect()
        resultado = session.query(Funcionario).get(id)
        resultado.ativo = False
        session.commit()
        session.close()

def salvar_pedido(data, id_cliente, usuario, preco, mesa, cupom):
      engine.connect()
      pedido = Pedido(ids_lanches=data, id_cliente=id_cliente, total=preco, atendente=usuario, data=datetime.now(), mesa=mesa, cupom=cupom)
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

def editar_produto(id, nome, descricao, preco, categoria, url_imagem, disponivel):
      engine.connect()
      query = session.query(Produto).get(id)
      query.nome = nome
      query.descricao = descricao
      query.preco = preco
      query.categoria = categoria
      query.url_imagem = url_imagem
      query.disponivel = disponivel

      session.commit()
      session.close()

lista_lanches = session.query(Produto).filter(and_(Produto.ativo == True, Produto.categoria == 'hamburguer'))
lista_bebidas = session.query(Produto).filter(and_(Produto.ativo == True, Produto.categoria == 'bebida'))
lista_adicionais = session.query(Adicional).filter(Adicional.ativo == True)
lista_funcionarios = session.query(Funcionario).filter(Funcionario.ativo == True)
lista_cupom = session.query(Cupom).filter(Cupom.ativo == True)
