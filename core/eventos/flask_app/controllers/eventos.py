## Coding Dojo - Python Bootcamp Jan 2025
## Eventos
## Roberto Alvarez, 2025

from flask_app import app
from flask import render_template, request, redirect, session, flash
from functools import wraps
from flask_app.models.evento import Evento
from flask_app.models.usuario import Usuario
from datetime import date
from flask_app.utils.decoradores import login_required

today = date.today()

@app.route('/eventos')
@login_required
def mostrar_eventos():
    session['detalhes'] = ""
    nome = session['nome']
    if nome is None:
        return redirect('/')
    eventos = Evento.get_all()
    return render_template("/eventos/eventos.html", nome=session['nome'], sobrenome=session['sobrenome'], id=session['id'], eventos=eventos, today=today)


@app.route("/adicionar_evento")
@login_required
def adicionar_evento():
    usuarios = Usuario.get_all()
    return render_template("/eventos/adicionar_evento.html", nome=session['nome'], sobrenome=session['sobrenome'], id=session['id'], usuarios=usuarios, detalhes=session['detalhes'])


@app.route("/criar_evento", methods=['POST'])
@login_required
def criar_evento():
    data = {
        'evento': request.form['evento'],
        'localizacao': request.form['localizacao'],
        'detalhes': request.form['detalhes'],
        'data': request.form['data'],
        'usuario_id': session['id']
    }
    if Evento.validar_evento(data, True) != True:
        return redirect("/adicionar_evento")
    Evento.save(data)
    flash(f'Novo evento adicionado com sucesso: "{data["evento"]}"', "success")
    session['detalhes'] = ""
    return redirect("/eventos")


@app.route("/editar_evento/<int:id>")
@login_required
def editar_evento(id):
    usuarios = Usuario.get_all()
    evento = Evento.get_one(id)
    detalhes = evento.detalhes
    if evento.usuario_id == session['id']:
        return render_template("/eventos/editar_evento.html", nome=session['nome'], sobrenome=session['sobrenome'], id=session['id'], usuarios=usuarios, evento=evento, detalhes=detalhes)
    else:
        flash(f'Somente o usuário que criou o evento pode editá-lo', "error")
    return redirect("/eventos")


@app.route("/update_evento", methods=['POST'])
@login_required
def atualizar_evento():
    data = {
        'id': request.form['id'],
        'evento': request.form['evento'],
        'localizacao': request.form['localizacao'],
        'detalhes': request.form['detalhes'],
        'data': request.form['data'],
        'usuario_id': session['id']
    }
    if Evento.validar_evento(data, False) != True:
        return redirect(f"/editar_evento/{data['id']}")
    Evento.update(data)
    flash(f"Evento atualizado com sucesso.", "success")
    session['detalhes'] = ""
    return redirect("/eventos")


@app.route("/eliminar_evento/<int:id>")
@login_required
def eliminar_evento(id):
    evento = Evento.get_one(id)
    Evento.delete(id)
    flash(f'O evento "{evento.evento}" foi eliminado.', "warning")
    return redirect('/eventos')


@app.route("/mostrar_evento/<int:id>")
@login_required
def mostrar_evento(id):
    evento = Evento.get_one(id)
    return render_template("/eventos/mostrar_evento.html", id=session['id'], evento=evento)