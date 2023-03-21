from flask import Flask, render_template, request, redirect
import requests, sqlalchemy
import database

app = Flask(__name__)

lanches = database.lista_lanches

@app.route("/")
def home():
    return render_template("index.html", lanches=lanches)

@app.route("/gerenciar/", methods=["POST", "GET"])
def gerenciar():
    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    preco = request.form.get("preco")
    url = request.form.get("url")
    
    if nome and preco and url:
        database.adicionar_produto(nome, descricao, preco, url)
        return redirect("/")
    return render_template("gerenciar.html", lanches=lanches)

@app.route("/consulta/<id>")
def consulta(id):
    retorno = database.session.query(database.Produto).get(id)
    if not retorno:
        return "Não encontrado"
    return f"Olá {retorno.nome} seu preço é de {retorno.preco}, foto: <img src=\"{retorno.url_imagem}\" />"

@app.route("/remover/<id>")
def remover(id):
    database.remover_lanche(id)
    return redirect(request.referrer)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)