
from flask import render_template, request, redirect, session, flash
from flask_app.utils.decoradores import login_required
from flask_app.models.noticia import Noticia
from flask_app.tasks.avaliacao_task import avaliar_texto_task
from flask import Blueprint

avaliacao = Blueprint('avaliacao', __name__)

@avaliacao.route('/avaliacao')
@login_required
def mostrar_avaliacao():
    return render_template("/avaliacao/avaliacao.html", nome=session['nome'])


@avaliacao.route('/avaliar_texto', methods=['POST'])
@login_required
def avaliar_texto():
    texto = request.form['texto']

    # Save the input and get its ID
    noticia_data = {
        'news': texto,
        'type': 0,
        'explanation': '',
        'usuario_id': session['id']
    }
    noticia_id = Noticia.save(noticia_data)

    # Launch Celery task asynchronously
    avaliar_texto_task.delay(noticia_id, texto, session['id'])

    flash("Seu texto foi enviado para avaliação. Aguarde alguns instantes e recarregue a página.")
    return redirect("/avaliacao_status/" + str(noticia_id))


@avaliacao.route('/avaliacao_status/<int:noticia_id>')
@login_required
def avaliacao_status(noticia_id):
    noticia = Noticia.get_one(noticia_id)

    return render_template(
        "avaliacao/avaliacao_status.html",
        nome=session['nome'],
        noticia=noticia
    )
