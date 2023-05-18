import os
from sqlalchemy import create_engine, Column, Integer, String, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexão BD
db_path = os.path.join(os.getcwd(), 'produtos.db')
engine = create_engine(f'sqlite:///{db_path}', echo=True)

Base = declarative_base()

class Funcionario(Base):
      __tablename__ = "funcionarios"

      id = Column(Integer, primary_key=True)
      nome = Column(String)
      usuario = Column(String)
      senha = Column(String)
      cargo = Column(String)

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    preco = Column(Double)
    descricao = Column(String)
    url_imagem = Column(String)

# Criando a tabela no banco de dados
Base.metadata.create_all(engine)

# Criando uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()

def cadastrar_funcionario(nome, usuario, senha, cargo):
      engine.connect()
      funcionario = Funcionario(nome=nome, usuario=usuario, senha=senha, cargo=cargo)
      session.add(funcionario)
      session.commit()
      session.close()

def validar_login(usuario, senha):
      engine.connect()
      res = session.query(Funcionario).filter(Funcionario.usuario == usuario).all()
      if res:
            res = res[0]
            if res.senha == senha:
                  return [True, res.nome, res.cargo]
            else:
                  return [False, "Usuário e/ou senha incorreto(s)."]
      return [False, "Usuário e/ou senha incorreto(s)."]


def adicionar_produto(nome, descricao, preco, url_imagem):
      engine.connect()
      produto = Produto(nome=nome, descricao=descricao, preco=preco, url_imagem=url_imagem)
      session.add(produto)
      session.commit()
      session.close()
      

def remover_lanche(id):
        resultado = session.query(Produto).get(id)
        session.delete(resultado)

lista_lanches = session.query(Produto)