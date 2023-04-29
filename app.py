from flask import Flask, render_template, request, redirect
import requests, sqlalchemy
import database

app = Flask(__name__)

lanches = database.lista_lanches
lista_carrinho = []
pedidos_cozinha = {}

@app.route("/")
def home():
    return render_template("index.html", lanches=lanches)

@app.route("/carrinho/", methods=["POST", "GET"])
def carrinho():
    carrinho_render = []
    for id in lista_carrinho:
        carrinho_render.append(database.session.query(database.Produto).get(id))
    
    return render_template("carrinho.html", carrinho=carrinho_render, lanches=lanches)

@app.route("/carrinho/adicionar/<id>")
def adicinar_carrinho(id):
    lista_carrinho.append(int(id))
    return redirect("/")

@app.route("/carrinho/remover/<id>")
def remover_carrinho(id):
    lista_carrinho.remove(int(id))
    return redirect("/carrinho")

@app.route("/carrinho/enviar/", methods=["POST", "GET"])
def enviar_cozinha():
    mesa_numero = request.form.get("mesa")
    produtos_enviar = []
    for id in lista_carrinho:
        query_result = database.session.query(database.Produto).get(id)
        produtos_enviar.append(query_result.nome)

    pedidos_cozinha[mesa_numero] = produtos_enviar
    lista_carrinho.clear()
    return redirect("/")

@app.route("/debug/")
def debug():
    return pedidos_cozinha

@app.route("/gerenciar/")
def gerenciar():
    return render_template("gerenciar.html", lanches=lanches)

@app.route("/adicionar/", methods=["POST", "GET"])
def adicionar():
    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    preco = request.form.get("preco")
    url = request.form.get("url")
    
    if nome and preco and url:
        database.adicionar_produto(nome, descricao, preco, url)
        return redirect("/")
    return render_template("adicionar.html", lanches=lanches)

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

@app.route("/cozinha/")
def cozinha():
    cozinha_render = []
    for mesa in pedidos_cozinha:
        for id in pedidos_cozinha[mesa]:
            cozinha_render.append(database.session.query(database.Produto).get(id))

    return render_template("cozinha.html", pedidos=pedidos_cozinha, lanches=cozinha_render)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)