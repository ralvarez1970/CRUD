## Usuarios
## Roberto Alvarez, 2025

from flask_app import app

from flask import render_template, request, redirect

from flask_app.models.estudante import Estudante
from flask_app.models.curso import Curso

@app.route("/estudantes")
def estudantes():
    estudantes = Estudante.get_all()
    return render_template("estudantes/estudantes.html", estudantes=estudantes)


@app.route('/criar_estudante')
def criar_estudante():
    cursos = Curso.get_all()
    return render_template("estudantes/criar.html", cursos=cursos, id=id)


@app.route('/incluir_estudante', methods=['POST'])
def incluir_estudante():
    data = {
        'nome': request.form['nome'],
        'sobrenome': request.form['sobrenome'],
        'email': request.form['email'],
        'idade': request.form['idade'],
        'created_at': 'NOW()',
        'updated_at': 'NOW()',
        'curso_id': request.form['curso']
        }
    if data['nome'] != "" and data['sobrenome'] != "" and data['email'] != "" and data['idade'] != "":
        Estudante.save(data)
        return redirect ('/estudantes')
    else:
        flash ("Dados incompletos")
    return redirect ('/criar_estudante')


@app.route('/incluir_estudante_curso/<int:id>')
def incluir_estudante_curso(id):
    curso = Curso.get_one(id)
    return render_template("estudantes/incluir.html", curso=curso, id=id)


@app.route("/editar_estudante/<int:id>")
def editar_estudante(id):
    estudante=Estudante.get_one(id)
    cursos = Curso.get_all()
    return render_template('estudantes/editar.html/', estudante=estudante, cursos=cursos)


@app.route("/atualizar_estudante/<int:id>", methods=['POST'])
def atualizar_estudante(id):
    estudante = Estudante.get_one(id)
    estudante.nome = request.form['nome']
    estudante.sobrenome = request.form['sobrenome'] 
    estudante.email = request.form['email'] 
    estudante.idade = request.form['idade'] 
    estudante.curso_id = request.form['curso'] 
    if estudante.nome != "" and estudante.sobrenome != "" and estudante.email != "" and estudante.idade  != "":
        Estudante.update(estudante)
        return redirect ('/estudantes')
    return redirect (f"/editar_estudante/{id}")


@app.route("/eliminar_estudante/<int:id>")
def eliminar_estudante(id):
    Estudante.delete(id)
    return redirect ('/estudantes')

@app.route("/cancelar_matricula/<int:id_curso>/<int:id_estudante>")
def cancelar_matricula(id_curso, id_estudante):
    Estudante.delete(id_estudante)
    return redirect (f'/curso/{id_curso}')
