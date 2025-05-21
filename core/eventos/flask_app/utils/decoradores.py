## Coding Dojo - Python Bootcamp Jan 2025
## Eventos
## Roberto Alvarez, 2025


from flask import render_template, flash, redirect, session
from functools import wraps  

def login_required(funcion):
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            flash("Você não está conectado", "error")
            return redirect("/")
        return funcion(*args, **kwargs)
    return wrapper


def has_permission(role):
    def wrapper_permission_main(funcion):
        @wraps(funcion)
        def wrapper_permission(*args, **kwargs):
            
            if session['user']['role'] != role:
                flash("Você não é um administrador.", "error")
                return redirect("/")
            
            return funcion(*args, **kwargs)
        return wrapper_permission
    return wrapper_permission_main