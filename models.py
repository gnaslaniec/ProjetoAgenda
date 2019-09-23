from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    def __init__(self, numero_telefone, categoria, contato_id):
        self.numero_telefone = numero_telefone
        self.categoria = categoria
        self.contato_id = contato_id
