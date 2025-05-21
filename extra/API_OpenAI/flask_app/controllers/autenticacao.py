## Coding Dojo - Python Bootcamp Jan 2025
## Roberto Alvarez, 2025

from flask import Blueprint, render_template, redirect, request, session, flash
from flask_app.models.usuario import Usuario
from flask_app.extensions import bcrypt

auth = Blueprint('auth', __name__)


@auth.route('/iniciar_sessao', methods=['POST'])
def login_usuario():
    usuario = Usuario.get_by_email(request.form['email'])
    if not usuario:
        flash("email e/ou senha errado(s)", "error")
        return redirect("/")
    if not bcrypt.check_password_hash(usuario.senha, request.form['senha']):
        flash("Endereço de email e/ou a senha estão errado(s)", "error")
        return redirect("/")
    flash("Você está logado no sistema", "success")
    session['email'] = usuario.email
    session['id'] = usuario.id
    session['nome'] = usuario.nome
    session['sobrenome'] = usuario.sobrenome
    session['sinopse'] = ""
    return redirect("/traducoes")


@auth.route('/fechar_sessao')
def close_session():
    if 'email' in session:
        session.clear()
        flash("Você foi desconectado do sistema.", "info")
    return redirect('/')
