## Coding Dojo - Python Bootcamp Jan 2025
## Eventos
## Roberto Alvarez, 2025


from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.usuario import Usuario
from datetime import date
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
today = date.today()

@app.route("/")
def registro():
    return render_template("/usuarios/registro.html")


@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    data = {
        'nome': request.form['nome'],
        'sobrenome': request.form['sobrenome'],
        'email': request.form['email'],
        'senha': request.form['senha'],
        'confirmacao_senha': request.form['confirmacao_senha'],
        }
    if Usuario.validar_usuario(data) == True:
        data.pop('confirmacao_senha', None)
        senha_hash = bcrypt.generate_password_hash(request.form['senha'])
        data['senha'] = senha_hash
        Usuario.save(data)
        flash("Usuário registrado com sucesso.", "success")
    return redirect("/")




