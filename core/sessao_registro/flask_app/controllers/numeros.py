## Coding Dojo - Python Bootcamp Jan 2025
## Sessao & Registro
## Roberto Alvarez, 2025


from flask_app import app
from flask import render_template, request, redirect, flash
from datetime import date
import random



today = date.today()

@app.route("/numero_sorte")
def numero():
    numero_sorte = random.randint(0, 100)
    flash(f"Hoje é {today.strftime('%B %d, %Y')} e o seu número da sorte é {numero_sorte}.", "warning")
    return redirect("/welcome")



