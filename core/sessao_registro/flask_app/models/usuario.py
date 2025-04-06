## Coding Dojo - Python Bootcamp Jan 2025
## Tutoriza
## Roberto Alvarez, 2025

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from datetime import date
from datetime import datetime


today = date.today()

class Usuario:

    def __init__(self , data):
        self.id = data['id']
        self.nome = data['nome']
        self.sobrenome = data['sobrenome']
        self.email = data['email']
        self.senha = data['senha']
        self.data_nascimento = data['data_nascimento']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_by_email(cls, email):
        query = "SELECT id, nome, sobrenome, email, senha, data_nascimento, created_at, updated_at FROM usuarios WHERE email = %(email)s;"
        data = {
            'email': email
        }
        resultados = connectToMySQL('eschema_usuarios').query_db(query, data)
        if len(resultados) == 0:
            return None
        usuario_recuperado = cls(resultados[0])
        return usuario_recuperado


    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuarios (nome, sobrenome, email, senha, data_nascimento, created_at, updated_at) VALUES (%(nome)s, %(sobrenome)s, %(email)s, %(senha)s, %(data_nascimento)s, NOW(), NOW())"
        return connectToMySQL('eschema_usuarios').query_db(query, data)
    

    @classmethod
    def check_email(cls, email):
        email_disponivel = True
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = {
            'email': email
        }
        results = connectToMySQL('eschema_usuarios').query_db(query, data)
        quantos = len(results)
        if quantos > 0:
            email_disponivel = False
        return email_disponivel


    @staticmethod
    def validar_usuario(usuario):
        valido = True
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
        senha_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$')
        data_nascimento = datetime.strptime(usuario['data_nascimento'], '%Y-%m-%d').date()
        if len(usuario['nome']) <= 2 or len(usuario['sobrenome']) <= 2:
            flash("Nome e sobrenome devem ter mais que dois caracteres.", "error")
            valido = False
        if usuario['senha'] != usuario['confirmacao_senha']:
            flash("As senhas informadas não coincidem.", "error")
            valido = False
        if data_nascimento > today:
            flash("A data de nascimento indicada é no futuro", "error")
            valido = False
        if not email_regex.match(usuario['email']):
            flash("Endereço de email inválido.", "error")
            valido = False
        if not senha_regex.match(usuario['senha']):
            flash("A senha deve ter no minimo 8 caracteres e conter pelo menos uma letra maiúscula, uma minúscula, um numera e um caractere especial.", "error")
            valido = False
        if Usuario.check_email(usuario['email']) == False:
            flash("Endereço de email já em uso. Tente outro.", "error")
            valido = False
        return valido