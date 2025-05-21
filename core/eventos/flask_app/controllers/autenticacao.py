## Coding Dojo - Python Bootcamp Jan 2025
## Eventos
## Roberto Alvarez, 2025

from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 


@app.route('/iniciar_sessao', methods=['POST'])
def login_usuario():
    usuario = Usuario.get_by_email(request.form['email'])
    if not usuario:
        flash("Email e/ou senha errado(s)", "error")
        return redirect("/")
    if not bcrypt.check_password_hash(usuario.senha, request.form['senha']):
        flash("Endereço de email e/ou a senha estão errado(s)", "error")
        return redirect("/")
    flash("Você está logado no sistema", "success")
    session['email'] = usuario.email
    session['id'] = usuario.id
    session['nome'] = usuario.nome
    session['sobrenome'] = usuario.sobrenome
    session['detalhes'] = ""
    return redirect("/eventos")


@app.route('/fechar_sessao')
def close_session():
    if 'email' in session:
        session.clear()
        flash("Você foi desconectado do sistema.", "info")
    return redirect ('/')