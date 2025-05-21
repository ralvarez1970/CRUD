## Coding Dojo - Python Bootcamp Jan 2025
## Roberto Alvarez, 2025

from flask import render_template, request, redirect, session, flash
from functools import wraps
from flask_app.models.usuario import Usuario
from datetime import date
from flask_app.utils.decoradores import login_required
import openai
import os
from flask import Blueprint

traducoes = Blueprint('traducoes', __name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI"))

@traducoes.route('/traducoes')
@login_required
def realizar_traducao():
    return render_template("/traducoes/traducoes.html", nome=session['nome'])


@traducoes.route('/traduzir_texto', methods=['POST'])
@login_required
def traduzir():
    texto = request.form['texto']
#    models = client.models.list()
#    for m in models.data:
#        print(m.id)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a translation assistant. Translate all user input from Portuguese to english. After the translation, you must include a blank line and, after that, a phase saying that the text was translated by hand by Roberto Alvarez"},
            {"role": "user", "content": f"{texto}"}
        ]
    )
    print()
    print("############################################")
    print("############################################")
    print(response)
    print("############################################")    
    traducao = response.choices[0].message.content
    session['texto_traduzido'] = traducao
    return redirect ("/mostrar_traducao")



@traducoes.route('/mostrar_traducao')
@login_required
def mostrar_traducao():
    return render_template("/traducoes/traducoes.html", nome=session['nome'], texto_traduzido=session['texto_traduzido'])