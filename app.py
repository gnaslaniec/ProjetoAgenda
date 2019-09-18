from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from config import Config

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost:3306/contatos"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
modus = Modus(app)
db = SQLAlchemy(app)

class Contato(db.Model):
    __tablename__= "contatos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    data_nascimento = db.Column(db.Text)
    enderecos = db.relationship('Endereco', backref="contato", lazy="dynamic")
    telefones = db.relationship('Telefone', backref="contato", lazy="dynamic")

    def __init__(self, nome, data_nascimento):
        self.nome = nome
        self.data_nascimento = data_nascimento

class Endereco(db.Model):
    __tablename__= "enderecos"

    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.Text)
    numero = db.Column(db.Integer)
    categoria = db.Column(db.Text)
    contato_id = db.Column(db.Integer, db.ForeignKey('contatos.id'))

    def __init__(self, rua,numero,categoria,contato_id):
        self.rua = rua
        self.numero = numero
        self.categoria = categoria
        self.contato_id = contato_id

class Telefone(db.Model):
    __tablename__= "telefones"

    id = db.Column(db.Integer, primary_key=True)
    numero_telefone = db.Column(db.Integer)
    categoria = db.Column(db.Text)
    contato_id = db.Column(db.Integer, db.ForeignKey('contatos.id'))

    def __init__(self, numero_telefone, categoria):
        self.numero_telefone = numero_telefone
        self.categoria = categoria


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


if __name__ == "__main__":
    app.run(debug=True, port=3000)