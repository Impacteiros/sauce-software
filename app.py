from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO
import database

app = Flask(__name__)
app.secret_key = "!yw2gC8!BeM3"
app.config['SECRET_KEY'] = "!yw2gC8!BeM3"

socketio = SocketIO(app)

lanches = database.lista_lanches
lista_carrinho = []
pedidos_cozinha = {}


def validar_perm():
    if session:
        if session['usuario'][1] == 'administrador':
            return True
    return False

@socketio.on('atualizacao')
def atualizar_cozinha():
    socketio.emit('atualizacao', {'data': "Dados atualizados"})


@app.route("/")
def home():
    try:
        session['usuario']
        nome = session['usuario'][0]
        cargo = session['usuario'][1]
    except KeyError:
        return redirect("/login/")
    return render_template("index.html", lanches=lanches, 
                           nome=nome, cargo=cargo)

@app.route("/login/", methods=["POST", "GET"])
def login():
    if 'usuario' in session:
        return redirect(url_for('home'))
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    if usuario and senha:
        validacao = database.validar_login(usuario, senha)
        if validacao[0]:
            session['usuario'] = [validacao[1], validacao[2]]
            return redirect(url_for("home"))
        return render_template("login.html", erro=validacao[1])
    return render_template("login.html")

@app.route("/cadastro/funcionario/", methods=["POST", "GET"])
def cadastro():
    nome = request.form.get("nome")
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")
    cargo = request.form.get("cargo")
    if nome and usuario and senha and cargo:
        database.cadastrar_funcionario(nome, usuario, senha, cargo)
        return "Cadastrado com sucesso"
    else:
        return render_template("cadastro_funcionario.html")


@app.route("/carrinho/", methods=["POST", "GET"])
def carrinho():
    carrinho_render = []
    preco_total = 0
    for id in lista_carrinho:
        produto = database.session.query(database.Produto).get(id)
        preco_total += produto.preco
        carrinho_render.append(produto)
    
    return render_template("carrinho.html", carrinho=carrinho_render, 
                           lanches=lanches, preco_total=preco_total)

@app.route("/deslogar/")
def deslogar():
    session.clear()
    return redirect("/login/")

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
    atualizar_cozinha()

    for id in lista_carrinho:
        query_result = database.session.query(database.Produto).get(id)
        produtos_enviar.append({"nome": query_result.nome, "id": id, "preco": query_result.preco})
    
    pedidos_cozinha[mesa_numero] = produtos_enviar
    lista_carrinho.clear()
    return redirect("/")

@app.route("/debug/")
def debug():
    return pedidos_cozinha

@app.route("/gerenciar/")
def gerenciar():
    if validar_perm():
            return render_template("gerenciar.html", lanches=lanches)
    return "Acesso negado", 403

@app.route("/adicionar/", methods=["POST", "GET"])
def adicionar():
    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    preco = request.form.get("preco")
    url = request.form.get("url")
    
    if nome and preco and url:
        database.adicionar_produto(nome, descricao, preco, url)
        return redirect("/")
    if validar_perm():
            return render_template("adicionar.html", lanches=lanches)
    return "Você não tem permissão.", 403

@app.route("/consulta/<id>")
def consulta(id):
    retorno = database.session.query(database.Produto).get(id)
    if not retorno:
        return "Não encontrado"
    return f"Olá {retorno.nome} seu preço é de {retorno.preco}, foto: <img src=\"{retorno.url_imagem}\" />"

@app.route("/remover/<id>")
def remover(id):
    if validar_perm():
        database.remover_lanche(id)
        return redirect(request.referrer)
    return "Acesso negado", 403

@app.route("/cozinha/")
def cozinha():
    query_resp = database.session.query(database.Pedidos).order_by(database.Pedidos.id.desc()).limit(5).all()
    ultimos_pedidos = {}
    lista_pedidos = []
    print(query_resp)
    for pedido in query_resp:
        nome_lanches = []
        ultimos_pedidos = {}
        lanches = pedido.ids_lanches.split(",")
        for id_lanche in lanches:
            lanche = database.get_lanche(id_lanche)
            nome_lanches.append(lanche.nome)
        
        ultimos_pedidos["mesa"] = pedido.mesa
        ultimos_pedidos["atendente"] = pedido.atendente
        ultimos_pedidos["lanches"] = nome_lanches
        lista_pedidos.append(ultimos_pedidos)

    return render_template("cozinha.html", pedidos=pedidos_cozinha, atendente=session['usuario'][0], finalizados=lista_pedidos)

@app.route("/cozinha/finalizar/<id>", methods=["POST", "GET"])
def finalizar_pedido(id):

    id_lanches = []
    for mesa in pedidos_cozinha:
        for produto in pedidos_cozinha[mesa]:
            id_lanches.append(str(produto['id']))

    preco_total = 0
    for mesa in pedidos_cozinha:
        for produto in pedidos_cozinha[mesa]:
            preco_total += produto['preco']
    pedidos_cozinha.pop(id)

    ids = ",".join(id_lanches)
    database.salvar_pedido(ids, session['usuario'][0], preco_total, id)
    return redirect(url_for("cozinha"))

if __name__ == "__main__":
    socketio.run(app)
    app.run(Debug=True)
