from flask import Flask
from dotenv import load_dotenv
import os

from flask_app.models import db
from flask_app.extensions import bcrypt  # Centralized bcrypt instance

load_dotenv()

def create_app():
    app = Flask(__name__)

    # 🔐 App configuration
    app.secret_key = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ⚙️ Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # 🧩 Import and register Blueprints
    from flask_app.controllers import (
        autenticacao,
        avaliacao_texto,
        extracoes,
        noticias,
        sesgo_fatos_narrados,
        sesgo_narrativa,
        traducoes,
        usuarios
    )

    app.register_blueprint(autenticacao.auth)
    app.register_blueprint(avaliacao_texto.avaliacao)
    app.register_blueprint(extracoes.extracoes)
    app.register_blueprint(noticias.noticias)
    app.register_blueprint(sesgo_fatos_narrados.sesgo_fatos)
    app.register_blueprint(sesgo_narrativa.sesgo_narrativa)
    app.register_blueprint(traducoes.traducoes)
    app.register_blueprint(usuarios.usuarios)

    # 🛠️ Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

# 🌐 Entry point for WSGI server or Celery
app = create_app()
