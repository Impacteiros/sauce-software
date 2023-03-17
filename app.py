from flask import Flask, render_template, request
import requests, sqlalchemy
import database

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!!"

@app.route("/inserir/")
def inserir():
    nome = request.args.get("nome")
    preco = request.args.get("preco")
    url = request.args.get("url")
    
    if nome and preco and url:
        produto = database.Produto(nome=nome, preco=preco, url_imagem=url)
        database.session.add(produto)
        database.session.commit()
        return "adicionado"
    return render_template("index.html")

@app.route("/consulta/<id>")
def consulta(id):
    retorno = database.session.query(database.Produto).get(id)
    if not retorno:
        return "Não encontrado"
    return f"Olá {retorno.nome} seu preço é de {retorno.preco}, foto: <img src=\"{retorno.url_imagem}\" />"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)