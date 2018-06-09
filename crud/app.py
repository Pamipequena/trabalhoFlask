

from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)


#########################

#LOGIN


class Login(db.Model):

	__tablename__ ='login'

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String)
	senha = db.Column(db.String)
	lembrar_me= db.Column(db.String)
	sair= db.Column(db.String)

	def __init__(self, email, senha, lembrar_me, sair):
		self.email = email
		self.senha = senha
		self.lembrar_me = lembrar_me
		self.sair = sair

db.create_all()


    
@app.route('/login', methods=['GET', 'POST'])
def login():

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('.login'))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('talks.index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    return redirect(url_for('/login.html'))

@app.route("/")
def loginn():
	return render_template("login.html")

@app.route("/index")
def index():
	return render_template("index.html")


#########################

#CADASTRO DE FUNCIONARIOS

class Pessoa(db.Model):

	__tablename__='users'

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	matricula = db.Column(db.String)
	nome = db.Column(db.String)
	senha= db.Column(db.String)
	funcionario = db.relationship('Vinculo', backref = 'users', lazy = True)

	def __init__(self, matricula, nome, senha):
		self.matricula = matricula
		self.nome = nome
		self.senha = senha

db.create_all()



@app.route("/cadastrar")
def cadastrar():
	return render_template("cadastro.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
	if request.method == "POST":
		matricula = request.form.get("matricula")
		nome = request.form.get("nome")
		senha = request.form.get("senha")
		
		if matricula and nome and senha:
			p = Pessoa(matricula, nome, senha)
			db.session.add(p)
			db.session.commit()

		return redirect (url_for("index"))

@app.route("/lista")
def lista():
	pessoas = Pessoa.query.all()
	return render_template("lista.html", pessoas=pessoas)

@app.route("/excluir/<int:id>")
def excluir(id):
	pessoa = Pessoa.query.filter_by(_id=id).first()

	db.session.delete(pessoa)
	db.session.commit()

	pessoas = Pessoa.query.all()
	return render_template("lista.html", pessoas=pessoas)

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
	pessoa = Pessoa.query.filter_by(_id=id).first()

	if request.method == "POST":
		matricula = request.form.get("matricula")
		nome = request.form.get("nome")
		senha = request.form.get("senha")

		if matricula and nome and senha:
			pessoa.matricula = matricula
			pessoa.nome = nome
			pessoa.senha = senha

			db.session.commit()

			return redirect(url_for("lista"))

	return render_template("atualizar.html", pessoa=pessoa)

################################

#CADASTRO DE CLIENTES

class Clientes(db.Model):

	__tablename__='client'

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	nome = db.Column(db.String)
	cpf= db.Column(db.String)
	projeto = db.relationship('Projeto', backref = 'client', lazy = True)

	def __init__(self, nome, cpf):
		self.nome = nome
		self.cpf = cpf

db.create_all()

@app.route("/cadastraClientes")
def cadastraClientes():
	return render_template("cadastro_clientes.html")

@app.route("/cadastro_clientes", methods=['GET', 'POST'])
def cadastro_clientes():
	if request.method == "POST":
		nome = request.form.get("nome")
		cpf = request.form.get("cpf")
		
		if nome and cpf:
			c = Clientes(nome, cpf)
			db.session.add(c)
			db.session.commit()

	return redirect (url_for("index"))

@app.route("/lista_clientes")
def lista_clientes():
	cliente = Clientes.query.all()
	return render_template("lista_clientes.html", cliente=cliente)

@app.route("/excluir_cliente/<int:id>")
def excluir_cliente(id):
	cliente = Clientes.query.filter_by(_id=id).first()

	db.session.delete(cliente)
	db.session.commit()

	cliente = Clientes.query.all()
	return render_template("lista_clientes.html", cliente=cliente)


@app.route("/atualizar_cliente/<int:id>", methods=['GET', 'POST'])
def atualizar_cliente(id):
	clientes = Clientes.query.filter_by(_id=id).first()

	if request.method == "POST":
		nome = request.form.get("nome")
		cpf = request.form.get("cpf")

		if nome and cpf:
			clientes.nome = nome
			clientes.cpf = cpf

			db.session.commit()

			return redirect(url_for("lista_clientes"))

	return render_template("atualizar_cliente.html", clientes=clientes)


#################################################################

#CADASTRO DE PROJETOS

class Projeto(db.Model):

	__tablename__='project'

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	codProjeto = db.Column(db.String)
	nomeProjeto = db.Column(db.String)
	clienteNome = db.Column(db.Integer, db.ForeignKey ('client._id'), nullable = False)
	descricaoProjeto = db.Column(db.String)
	projeto = db.relationship('Vinculo', backref = 'project', lazy = True)


	def __init__(self, codProjeto, nomeProjeto, clienteNome, descricaoProjeto):
		self.codProjeto = codProjeto
		self.nomeProjeto = nomeProjeto
		self.clienteNome = clienteNome 
		self.descricaoProjeto = descricaoProjeto

#db.create_all()

@app.route("/cadastraProjeto")
def cadastraProjeto():
	return render_template("cadastro_projetos.html")

@app.route("/cadastro_projetos", methods=['GET', 'POST'])
def cadastro_projetos():
	if request.method == "POST":
		codProjeto = request.form.get("codProjeto")
		nomeProjeto = request.form.get("nomeProjeto")
		clienteNome = request.form.get("clienteNome")
		descricaoProjeto = request.form.get("descricaoProjeto")


		if codProjeto and nomeProjeto and clienteNome and descricaoProjeto:
			pj = Projeto(codProjeto, nomeProjeto, clienteNome, descricaoProjeto )
			db.session.add(pj)
			db.session.commit()

	return redirect (url_for("index"))

@app.route("/lista_projetos")
def lista_projetos():
	projetos = Projeto.query.all()
	return render_template("lista_projetos.html", projetos=projetos)

@app.route("/excluir_projeto/<int:id>")
def excluir_projeto(id):
	projetos = Projeto.query.filter_by(_id=id).first()

	db.session.delete(projetos)
	db.session.commit()

	projetos = Projeto.query.all()
	return render_template("lista_clientes.html", projetos=projetos)


@app.route("/atualizar_projeto/<int:id>", methods=['GET', 'POST'])
def atualizar_projeto(id):
	projeto = Projeto.query.filter_by(_id=id).first()

	if request.method == "POST":
		codProjeto = request.form.get("codProjeto")
		nomeProjeto = request.form.get("nomeProjeto")
		clienteNome = request.form.get("clienteNome")
		descricaoProjeto = request.form.get("descricaoProjeto")

		if nome and cpf:
			projeto.codProjeto = codProjeto
			projeto.nomeProjeto = nomeProjeto
			projeto.clienteNome = clienteNome
			projeto.descricaoProjeto = descricaoProjeto

			db.session.commit()

			return redirect(url_for("lista_projetos"))

	return render_template("atualizar_projeto.html", projeto=projeto)

####################################################3

#CADASTRO DE ATIVIDADES

class Atividade(db.Model):

	__tablename__='atividad'

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	codAtividade = db.Column(db.String)
	descricao = db.Column(db.String)
	
	def __init__(self, codAtividade, descricao):
		self.codAtividade = codAtividade
		self.descricao = descricao


db.create_all()

@app.route("/cadastraAtividade")
def cadastraAtividade():
	return render_template("cadastro_atividades.html")

@app.route("/cadastro_atividades", methods=['GET', 'POST'])
def cadastro_atividades():
	if request.method == "POST":
		codAtividade = request.form.get("codAtividade")
		descricao = request.form.get("descricao")


		if codAtividade and descricao:
			at = Atividade(codAtividade, descricao)
			db.session.add(at)
			db.session.commit()

	return redirect (url_for("index"))

@app.route("/lista_atividades")
def lista_atividades():
	atividades = Atividade.query.all()
	return render_template("lista_atividades.html", atividades=atividades)

@app.route("/excluir_atividade/<int:id>")
def excluir_atividade(id):
	atividades = Atividade.query.filter_by(_id=id).first()

	db.session.delete(atividades)
	db.session.commit()

	atividades = Atividades.query.all()
	return render_template("lista_clientes.html", atividades=atividades)


@app.route("/atualizar_atividade/<int:id>", methods=['GET', 'POST'])
def atualizar_atividade(id):
	atividade = Atividade.query.filter_by(_id=id).first()

	if request.method == "POST":
		codAtividade = request.form.get("codAtividade")
		descricao = request.form.get("descricao")


		if nome and cpf:
			atividade.codAtividade = codAtividade
			atividade.descricao = descricao

			db.session.commit()

			return redirect(url_for("lista_atividades"))

	return render_template("atualizar_atividade.html", atividade=atividade)

###############################################

#VINCULO PROJETOxFUNCIONARIO

class Vinculo(db.Model):

	__tablename__='vinculo'

	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	codProjetoxFuncionario = db.Column(db.String)
	nomeFuncionario = db.Column(db.Integer, db.ForeignKey ('users._id'), nullable = False)
	nomeProjeto = db.Column(db.Integer, db.ForeignKey ('project._id'), nullable = False)
	


	def __init__(self, codProjetoxFuncionario, nomeFuncionario, nomeProjeto):
		self.codProjetoxFuncionario = codProjetoxFuncionario
		self.nomeFuncionario = nomeFuncionario
		self.nomeProjeto = nomeProjeto


db.create_all()

@app.route("/cadastraVinculo")
def cadastraVinculo():
	return render_template("cadastro_vinculo.html")

@app.route("/cadastro_vinculo", methods=['GET', 'POST'])
def cadastro_vinculo():
	if request.method == "POST":
		codProjetoxFuncionario = request.form.get("codProjetoxFuncionario")
		nomeFuncionario = request.form.get("nomeFuncionario")
		nomeProjeto = request.form.get("nomeProjeto")


		if codProjetoxFuncionario and nomeFuncionario and nomeProjeto:
			v = Vinculo(codProjetoxFuncionario, nomeFuncionario, nomeProjeto)
			db.session.add(v)
			db.session.commit()

	return redirect (url_for("index"))

@app.route("/lista_vinculo")
def lista_vinculo():
	vinculos = Vinculo.query.all()
	return render_template("lista_vinculo.html", vinculos=vinculos)

@app.route("/excluir_vinculo/<int:id>")
def excluir_vinculo(id):
	vinculos = Vinculo.query.filter_by(_id=id).first()

	db.session.delete(vinculos)
	db.session.commit()

	vinculos = Vinculo.query.all()
	return render_template("lista_vinculo.html", vinculos=vinculos)


@app.route("/atualizar_vinculo/<int:id>", methods=['GET', 'POST'])
def atualizar_vinculo(id):
	vinculo = Vinculo.query.filter_by(_id=id).first()

	if request.method == "POST":
		codProjetoxFuncionario = request.form.get("codProjetoxFuncionario")
		nomeFuncionario = request.form.get("nomeFuncionario")
		nomeProjeto = request.form.get("nomeProjeto")


		if nome and cpf:
			vinculo.codProjetoxFuncionario = codProjetoxFuncionario
			vinculo.nomeFuncionario = nomeFuncionario
			vinculo.nomeProjeto = nomeProjeto

			db.session.commit()

			return redirect(url_for("lista_vinculo"))

	return render_template("atualizar_vinculo.html", vinculo=vinculo)

if __name__ == '__main__':
	app.run(debug=True)

