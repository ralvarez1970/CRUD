## Coding Dojo - Python Bootcamp Jan 2025
## Roberto Alvarez, 2025

from flask import render_template, request, redirect, session, flash
from flask_app.utils.decoradores import login_required
from flask_app.models.noticia import Noticia
from flask_app.utils.openai_helper import call_openai_with_tool
from datetime import date
from flask import Blueprint

noticias = Blueprint('noticias', __name__)

numero_noticias = 0


@noticias.route('/noticias')
@login_required
def mostrar_noticias():
    return render_template("/noticias/noticias.html", nome=session['nome'], numero_noticias=numero_noticias)

@noticias.route('/guardar_noticia', methods=['POST'])
@login_required
def guardar_noticia():
    global numero_noticias
    texto = request.form['texto']
    data = {
        'news': texto,
        'type': 0,
        'explanation': 'Yo no se...',
        'usuario_id': session['id'],
    }
    Noticia.save(data)
    flash ("Notícia salva com sucesso.", "success")
    numero_noticias += 1
    return redirect ("/noticias")