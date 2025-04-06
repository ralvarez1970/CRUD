## Coding Dojo - Python Bootcamp Jan 2025
## Tutoriza
## Roberto Alvarez, 2025


from flask import render_template, flash, redirect, session
from functools import wraps  

def login_required(funcion):
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            flash("Você não está logado", "error")
            return redirect("/")
        return funcion(*args, **kwargs)
    return wrapper


def tem_permissao(role):
    def wrapper_permissao_main(funcion):
        @wraps(funcion)
        def wrapper_permisao(*args, **kwargs):
            
            if session['usuario']['role'] != role:
                flash("Você não é administrador.", "error")
                return redirect("/")
            
            return funcion(*args, **kwargs)
        return wrapper_permisqo
    return wrapper_permisao_main