## Estudantes & Cursos
## Roberto Alvarez, 2025

from flask_app import app

from flask import render_template, request, redirect, flash

from flask_app.models.estudante import Estudante
from flask_app.models.curso import Curso

@app.route("/")
def cursos():
    cursos = Curso.get_all()
    return render_template("cursos/cursos.html", cursos=cursos)

@app.route('/criar_curso')
def criar_curso():
    return render_template("cursos/criar.html")

@app.route('/incluir_curso', methods=['POST'])
def incluir_curso():
    data = {
        'nome': request.form['nome'],
        'created_at': 'NOW()',
        'updated_at': 'NOW()',
        }
    if data['nome'] != "":
        Curso.save(data)
    return redirect ('/')



@app.route('/curso/<int:id>')
def detalhar_curso(id):
    curso=Curso.get_one(id)
    estudantes=Estudante.select(id)
    print()
    print("############################################")
    print("############################################")
    print("Estudantes: ", estudantes)
    print("############################################")
    print()
    return render_template('cursos/mostrar.html', curso=curso, estudantes=estudantes)


@app.route("/editar_curso/<int:id>")
def editar_curso(id):
    curso=Curso.get_one(id)
    return render_template('cursos/editar.html', curso=curso)


@app.route("/atualizar_curso/<int:id>", methods=['POST'])
def atualizar_curso(id):
    curso = Curso.get_one(id)
    curso.nome = request.form['nome']
    Curso.update(curso)
    return redirect ('/')


@app.route("/eliminar_curso/<int:id>")
def eliminar_curso(id):
    Curso.delete(id)
    return redirect ('/')
