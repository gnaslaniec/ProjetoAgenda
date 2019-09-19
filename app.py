from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus

from models import Contato,Endereco,Telefone, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost:3306/contatos"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
modus = Modus(app)
db.init_app(app)

@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/contatos', methods=["GET","POST"])
def index():
    if request.method == "POST":
        novo_contato = Contato(request.form['nome'], request.form['data_nascimento'])
        db.session.add(novo_contato)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('contatos/index.html', contatos=Contato.query.all())

@app.route('/contatos/novo')
def novo():
    return render_template('contatos/novo.html')

@app.route('/contatos/<int:id>/editar')
def editar(id):
    return render_template('/contatos/editar.html', contato=Contato.query.get(id))

@app.route('/contatos/<int:id>', methods=['GET','PATCH','DELETE'])
def exibir(id):
    contato_id = Contato.query.get(id)
    if request.method == b"PATCH":
        contato_id.nome = request.form['nome']
        contato_id.data_nascimento = request.form['data_nascimento']
        db.session.add(contato_id)
        db.session.commit()
        return redirect(url_for('index'))
    if request.method == b"DELETE":
        db.session.delete(contato_id)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('/contatos/exibir.html', contato=Contato.query.get(id))

''' ROTAS ENDEREÇO '''
@app.route('/contatos/<int:contato_id>/enderecos', methods=["GET","POST"])
def enderecos_index(contato_id):
    if request.method == 'POST':
        new_endereco = Endereco(request.form['rua'],request.form['numero'],request.form['categoria'] ,contato_id)
        db.session.add(new_endereco)
        db.session.commit()
        return redirect(url_for('enderecos_index', contato_id=contato_id))
    return render_template('enderecos/index.html', contato=Contato.query.get(contato_id))

@app.route('/contatos/<int:contato_id>/enderecos/novo', methods=["GET","POST"])
def enderecos_novo(contato_id):
    return render_template('enderecos/novo.html', contato=Contato.query.get(contato_id))

@app.route('/contatos/<int:contato_id>/enderecos/<int:id>/editar')
def enderecos_editar(contato_id,id):
    endereco_editar = Endereco.query.get(id)
    return render_template('enderecos/editar.html', endereco=endereco_editar)

@app.route('/contatos/<int:contato_id>/enderecos/<int:id>', methods=["GET","PATCH","DELETE"])
def enderecos_exibir(contato_id,id):
    endereco_encontrado = Endereco.query.get(id)
    if request.method == b"PATCH":
        endereco_encontrado.rua = request.form['rua']
        endereco_encontrado.numero = request.form['numero']
        endereco_encontrado.categoria = request.form['categoria']
        db.session.add(endereco_encontrado)
        db.session.commit()
        return redirect(url_for('enderecos_index', contato_id=endereco_encontrado.contato_id))
    if request.method == b"DELETE":
        db.session.delete(endereco_encontrado)
        db.session.commit()
        return redirect(url_for('enderecos_index', contato_id=endereco_encontrado.contato_id))
    return render_template('enderecos/exibir.html', endereco=endereco_encontrado)

''' Rotas Telefone '''
@app.route('/contatos/<int:contato_id>/telefones', methods=["GET","POST"])
def telefones_index(contato_id):
    if request.method == 'POST':
        new_telefone = Telefone(request.form['numero_telefone'], request.form['categoria'], contato_id)
        db.session.add(new_telefone)
        db.session.commit()
        return redirect(url_for('telefones_index', contato_id=contato_id))
    return render_template('telefones/index.html', contato=Contato.query.get(contato_id))

@app.route('/contatos/<int:contato_id>/telefones/novo', methods=["GET","POST"])
def telefones_novo(contato_id):
    return render_template('telefones/novo.html', contato=Contato.query.get(contato_id))

@app.route('/contatos/<int:contato_id>/telefones/<int:id>/editar')
def telefones_editar(contato_id,id):
    telefone_editar = Telefone.query.get(id)
    return render_template('telefones/editar.html', telefone=telefone_editar)

@app.route('/contatos/<int:contato_id>/telefones/<int:id>', methods=["GET","PATCH","DELETE"])
def telefones_exibir(contato_id,id):
    telefone_encontrado = Telefone.query.get(id)
    if request.method == b"PATCH":
        telefone_encontrado.numero_telefone = request.form['numero_telefone']
        telefone_encontrado.categoria = request.form['categoria']
        db.session.add(telefone_encontrado)
        db.session.commit()
        return redirect(url_for('telefones_index', contato_id=telefone_encontrado.contato_id))
    if request.method == b"DELETE":
        db.session.delete(telefone_encontrado)
        db.session.commit()
        return redirect(url_for('telefones_index', contato_id=telefone_encontrado.contato_id))
    return render_template('telefones/exibir.html', endereco=telefone_encontrado)

if __name__ == "__main__":
    app.run(debug=True, port=3000)