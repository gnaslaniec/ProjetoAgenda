from flask import Flask, request, redirect, render_template, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, fields
from flask_modus import Modus

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost:3306/contatos"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

modus = Modus(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Contato(db.Model):
    __tablename__= "contatos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text)
    dia = db.Column(db.Integer)
    mes = db.Column(db.Text)
    ano = db.Column(db.Integer)
    enderecos = db.relationship('Endereco', cascade="all,delete", backref="contato", lazy="dynamic")
    telefones = db.relationship('Telefone', cascade="all,delete", backref="contato", lazy="dynamic")

    def __init__(self, nome, dia, mes, ano):
        self.nome = nome
        self.dia = dia
        self.mes = mes 
        self.ano = ano


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
    numero_telefone = db.Column(db.Text)
    categoria = db.Column(db.Text)
    contato_id = db.Column(db.Integer, db.ForeignKey('contatos.id'))

    def __init__(self, numero_telefone, categoria, contato_id):
        self.numero_telefone = numero_telefone
        self.categoria = categoria
        self.contato_id = contato_id

class ContatoSchema(ma.ModelSchema):
    class Meta:
        model = Contato
        fields = ('id', 'nome','dia','mes','ano')
        
@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/contatos', methods=["GET","POST"])
def index():
    if request.method == "POST":
        novo_contato = Contato(request.form['nome'], request.form['dia'], request.form['mes'], request.form['ano'])
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
        contato_id.dia = request.form['dia']
        contato_id.mes = request.form['mes']
        contato_id.ano = request.form['ano']
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


''' Rotas API '''
@app.route('/contatos/api/getContatos')
def getContatos():
    contato_schema = ContatoSchema(many=True)
    contatos = Contato.query.all()
    contato_json = contato_schema.dumps(contatos, ensure_ascii=False).encode('utf8')

    return contato_json.decode()
    

@app.route('/contatos/api/getContatos/<int:contato_id>')
def getContatosID(contato_id):
    contato_schema = ContatoSchema()
    contato = Contato.query.filter_by(id=contato_id).first()
    contato_json = contato_schema.dumps(contato, ensure_ascii=False).encode('utf8')

    return contato_json.decode()
    

@app.route('/contatos/api/getContatos/<string:contato_nome>')
def getContatosNome(contato_nome):
    contato_schema = ContatoSchema()
    contato = Contato.query.filter(Contato.nome.contains(contato_nome)).first()
    #contato = Contato.query.filter_by(nome=contato_nome).first()
    contato_json = contato_schema.dumps(contato, ensure_ascii=False).encode('utf8')

    return contato_json.decode()


@app.route('/contatos/api/getContatos/mes/<string:contato_mes>')
def getContatosMes(contato_mes):
    contato_schema = ContatoSchema(many=True)
    contato = Contato.query.filter_by(mes=contato_mes).all()
    contato_json = contato_schema.dumps(contato, ensure_ascii=False).encode('utf8')

    return contato_json.decode()


if __name__ == "__main__":
    app.run(debug=True, port=3000)