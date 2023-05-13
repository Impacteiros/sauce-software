import os
from sqlalchemy import create_engine, Column, Integer, String, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexão BD
db_path = os.path.join(os.getcwd(), 'produtos.db')
engine = create_engine(f'sqlite:///{db_path}', echo=True)

Base = declarative_base()

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