from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from models import db, Cliente, Produto, Orcamento

app = Flask(__name__)

# Configuração básica do banco SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orcamentos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# ==================== HOME ====================
@app.route("/")
def index():
    return render_template("index.html")


# ==================== CLIENTES ====================

# LISTAR CLIENTES
@app.route("/clientes")
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template("clientes_list.html", clientes=clientes)


# FORMULÁRIO NOVO CLIENTE
@app.route("/clientes/novo")
def novo_cliente():
    return render_template("clientes_form.html")


# CRIAR CLIENTE
@app.route("/clientes", methods=["POST"])
def criar_cliente():
    nome = request.form.get("nome")
    email = request.form.get("email")
    telefone = request.form.get("telefone")

    if not nome:
        return redirect(url_for("listar_clientes"))

    cliente = Cliente(nome=nome, email=email, telefone=telefone)
    db.session.add(cliente)
    db.session.commit()

    return redirect(url_for("listar_clientes"))


# FORMULÁRIO EDITAR CLIENTE
@app.route("/clientes/<int:cliente_id>/editar")
def editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    return render_template("clientes_form.html", cliente=cliente)


# ATUALIZAR CLIENTE
@app.route("/clientes/<int:cliente_id>/atualizar", methods=["POST"])
def atualizar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)

    nome = request.form.get("nome")
    email = request.form.get("email")
    telefone = request.form.get("telefone")

    if not nome:
        return redirect(url_for("listar_clientes"))

    cliente.nome = nome
    cliente.email = email
    cliente.telefone = telefone

    db.session.commit()

    return redirect(url_for("listar_clientes"))


# EXCLUIR CLIENTE
@app.route("/clientes/<int:cliente_id>/excluir", methods=["POST"])
def excluir_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)

    # impede excluir cliente que já tem orçamentos
    if cliente.orcamentos:
        return redirect(url_for("listar_clientes"))

    db.session.delete(cliente)
    db.session.commit()

    return redirect(url_for("listar_clientes"))


# ==================== PRODUTOS ====================

# LISTAR PRODUTOS
@app.route("/produtos")
def listar_produtos():
    produtos = Produto.query.all()
    return render_template("produtos_list.html", produtos=produtos)


# FORMULÁRIO NOVO PRODUTO
@app.route("/produtos/novo")
def novo_produto():
    return render_template("produtos_form.html")


# CRIAR PRODUTO
@app.route("/produtos", methods=["POST"])
def criar_produto():
    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    preco_base = request.form.get("preco_base")

    if not nome or not preco_base:
        return redirect(url_for("listar_produtos"))

    produto = Produto(
        nome=nome,
        descricao=descricao,
        preco_base=float(preco_base),
    )
    db.session.add(produto)
    db.session.commit()

    return redirect(url_for("listar_produtos"))


# FORMULÁRIO EDITAR PRODUTO
@app.route("/produtos/<int:produto_id>/editar")
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    return render_template("produtos_form.html", produto=produto)


# ATUALIZAR PRODUTO
@app.route("/produtos/<int:produto_id>/atualizar", methods=["POST"])
def atualizar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)

    nome = request.form.get("nome")
    descricao = request.form.get("descricao")
    preco_base = request.form.get("preco_base")

    if not nome or not preco_base:
        return redirect(url_for("listar_produtos"))

    produto.nome = nome
    produto.descricao = descricao
    produto.preco_base = float(preco_base)

    db.session.commit()

    return redirect(url_for("listar_produtos"))


# EXCLUIR PRODUTO
@app.route("/produtos/<int:produto_id>/excluir", methods=["POST"])
def excluir_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)

    # impede excluir produto que já tem orçamentos
    if produto.orcamentos:
        return redirect(url_for("listar_produtos"))

    db.session.delete(produto)
    db.session.commit()

    return redirect(url_for("listar_produtos"))


# ==================== ORÇAMENTOS ====================

# LISTAR ORÇAMENTOS
@app.route("/orcamentos")
def listar_orcamentos():
    orcamentos = Orcamento.query.order_by(Orcamento.data_criacao.desc()).all()
    return render_template("orcamentos_list.html", orcamentos=orcamentos)


# FORMULÁRIO NOVO ORÇAMENTO
@app.route("/orcamentos/novo")
def novo_orcamento():
    clientes = Cliente.query.all()
    produtos = Produto.query.all()
    return render_template("orcamentos_form.html", clientes=clientes, produtos=produtos)


# CRIAR ORÇAMENTO
@app.route("/orcamentos", methods=["POST"])
def criar_orcamento():
    cliente_id = request.form.get("cliente_id")
    produto_id = request.form.get("produto_id")
    valor_total = request.form.get("valor_total")
    status = request.form.get("status") or "Pendente"

    if not cliente_id or not produto_id or not valor_total:
        return redirect(url_for("listar_orcamentos"))

    orc = Orcamento(
        cliente_id=int(cliente_id),
        produto_id=int(produto_id),
        valor_total=float(valor_total),
        status=status,
        data_criacao=datetime.now(),
    )
    db.session.add(orc)
    db.session.commit()

    return redirect(url_for("listar_orcamentos"))


# FORMULÁRIO EDITAR ORÇAMENTO
@app.route("/orcamentos/<int:orcamento_id>/editar")
def editar_orcamento(orcamento_id):
    orcamento = Orcamento.query.get_or_404(orcamento_id)
    clientes = Cliente.query.all()
    produtos = Produto.query.all()
    return render_template(
        "orcamentos_form.html",
        orcamento=orcamento,
        clientes=clientes,
        produtos=produtos,
    )


# ATUALIZAR ORÇAMENTO
@app.route("/orcamentos/<int:orcamento_id>/atualizar", methods=["POST"])
def atualizar_orcamento(orcamento_id):
    orcamento = Orcamento.query.get_or_404(orcamento_id)

    cliente_id = request.form.get("cliente_id")
    produto_id = request.form.get("produto_id")
    valor_total = request.form.get("valor_total")
    status = request.form.get("status") or "Pendente"

    if not cliente_id or not produto_id or not valor_total:
        return redirect(url_for("listar_orcamentos"))

    orcamento.cliente_id = int(cliente_id)
    orcamento.produto_id = int(produto_id)
    orcamento.valor_total = float(valor_total)
    orcamento.status = status

    db.session.commit()

    return redirect(url_for("listar_orcamentos"))


# EXCLUIR ORÇAMENTO
@app.route("/orcamentos/<int:orcamento_id>/excluir", methods=["POST"])
def excluir_orcamento(orcamento_id):
    orcamento = Orcamento.query.get_or_404(orcamento_id)
    db.session.delete(orcamento)
    db.session.commit()
    return redirect(url_for("listar_orcamentos"))


# ==================== CONTROLE POR STATUS ====================

@app.route("/controle")
def controle_status():
    pendentes = Orcamento.query.filter_by(status="Pendente").all()
    aprovados = Orcamento.query.filter_by(status="Aprovado").all()
    rejeitados = Orcamento.query.filter_by(status="Rejeitado").all()

    return render_template(
        "controle_status.html",
        pendentes=pendentes,
        aprovados=aprovados,
        rejeitados=rejeitados,
    )


# ==================== INICIALIZAÇÃO ====================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)