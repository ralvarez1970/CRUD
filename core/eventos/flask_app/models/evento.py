## Coding Dojo - Python Bootcamp Jan 2025
## Eventos
## Roberto Alvarez, 2025

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from datetime import date, datetime
from flask_app.models.usuario import Usuario

today = date.today()

class Evento:

    def __init__(self, data):
        self.id = data['id']
        self.evento = data['evento']
        self.localizacao = data['localizacao']
        self.data = data['data']
        self.detalhes = data['detalhes']
        self.usuario_id = data['usuario_id']
        self.nome_usuario = data['nome_usuario']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = """
        SELECT eventos.id AS id, eventos.evento AS evento, eventos.localizacao AS localizacao, eventos.detalhes AS detalhes,
               eventos.data AS data, eventos.created_at AS created_at, eventos.updated_at AS updated_at,
               eventos.usuario_id AS usuario_id, usuarios.nome AS nome_usuario
        FROM eventos
        LEFT JOIN usuarios ON eventos.usuario_id = usuarios.id
        ORDER BY eventos.data ASC;
        """
        results = connectToMySQL().query_db(query)
        eventos = []
        for evento in results:
            eventos.append(cls(evento))
        return eventos

    @classmethod
    def get_one(cls, id):
        query = """
        SELECT eventos.id AS id, eventos.evento AS evento, eventos.localizacao AS localizacao, eventos.detalhes AS detalhes,
               eventos.data AS data, eventos.created_at AS created_at, eventos.updated_at AS updated_at,
               eventos.usuario_id AS usuario_id, usuarios.nome AS nome_usuario
        FROM eventos
        LEFT JOIN usuarios ON eventos.usuario_id = usuarios.id
        WHERE eventos.id = %(id)s;
        """
        data = {"id": id}
        result = connectToMySQL().query_db(query, data)
        return cls(result[0]) if result else None

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO eventos (evento, localizacao, detalhes, data, created_at, updated_at, usuario_id)
        VALUES (%(evento)s, %(localizacao)s, %(detalhes)s, %(data)s, NOW(), NOW(), %(usuario_id)s);
        """
        return connectToMySQL().query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM eventos WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL().query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
        UPDATE eventos
        SET evento = %(evento)s, localizacao = %(localizacao)s, detalhes = %(detalhes)s, data = %(data)s,
            updated_at = NOW()
        WHERE id = %(id)s;
        """
        return connectToMySQL().query_db(query, data)

    @classmethod
    def check_evento_duplicado(cls, evento, evento_id, usuario_id):
        evento_disponivel = True
        evento_limpo = evento.replace(" ", "").lower()
        query = "SELECT * FROM eventos WHERE LOWER(REPLACE(evento, ' ', '')) = %(evento_limpo)s AND usuario_id = %(usuario_id)s AND id != %(id)s;"
        data = {
            'evento_limpo': evento_limpo,
            'usuario_id': usuario_id,
            'id': evento_id
        }
        results = connectToMySQL().query_db(query, data)
        quantos = len(results)
        if quantos > 0:
            evento_disponivel = False
        return evento_disponivel

    @staticmethod
    def validar_evento(evento, incluir):
        valido = True
        session['detalhes'] = evento['detalhes']
        if incluir == True:
            evento_atual = 1
        else:
            evento_atual = evento['id']
        evento['data'] = datetime.strptime(evento['data'], '%Y-%m-%d').date()
        if len(evento['evento']) <= 3:
            flash("O nome do evento deve ter mais que três caracteres.", "error")
            valido = False
        if len(evento['localizacao']) <= 3:
            flash("A localização deve ter mais que três caracteres.", "error")
            valido = False
        if len(evento['detalhes']) <= 3:
            flash("Os detalhes devem ter mais que três caracteres.", "error")
            valido = False
        if len(evento['detalhes']) > 500:
            flash("O tamanho máximo dos detalhes é 500 caracteres. Ajuste a descrição e tente novamente.", "error")
            valido = False
        if evento['data'] < today:
            flash("Você não pode criar um evento com data no passado. Verifique e corrija a data.", "error")
            valido = False
        if Evento.check_evento_duplicado(evento['evento'], evento_atual, evento['usuario_id']) == False:
            flash("Você já criou um evento com este nome. Por favor escolha um nome diferente.", "error")
            valido = False
        return valido