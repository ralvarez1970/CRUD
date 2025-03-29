from flask import Flask, render_template, request, redirect, url_for

from usuario import Usuario

app = Flask(__name__)

@app.route("/")
def index():
    usuarios = Usuario.get_all()
    return render_template("index.html", usuarios=usuarios)

@app.route('/criar')
def criar_usuario():
    return render_template("criar.html")

@app.route('/incluir', methods=['POST'])
def incluir_usuario():
    data = {
        'nome': request.form['nome'],
        'sobrenome': request.form['sobrenome'],
        'email': request.form['email'],
        'created_at': 'NOW()',
        'updated_at': 'NOW()',
        }
    Usuario.save(data)
    return redirect ('/')

@app.route('/usuario/<int:id>')
def detalhes_usuario(id):
    usuario=Usuario.get_one(id)
    return render_template('detalhar.html', usuario=usuario)


@app.route("/editar/<int:id>")
def editar_usuario(id):
    usuario=Usuario.get_one(id)
    return render_template('editar.html', usuario=usuario)


@app.route("/atualizar/<int:id>", methods=['POST'])
def atualizar_usuario(id):
    usuario = Usuario.get_one(id)
    usuario.nome = request.form['nome']
    usuario.sobrenome = request.form['sobrenome'] 
    usuario.email = request.form['email'] 
    Usuario.update(usuario)
    return redirect ('/')


@app.route("/eliminar/<int:id>")
def eliminar_usuario(id):
    Usuario.delete(id)
    return redirect ('/')

if __name__ == "__main__":
    app.run(debug=True)