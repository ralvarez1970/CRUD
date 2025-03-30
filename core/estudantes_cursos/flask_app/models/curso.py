## Estudantes & Cursos
## Roberto Alvarez, 2025

from flask_app.config.mysqlconnection import connectToMySQL

class Curso:

    def __init__( self , data ):
        self.id = data['id']
        self.nome = data['nome']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cursos;"
        results = connectToMySQL('db_esquema_estudantes_cursos').query_db(query)
        cursos = []
        for curso in results:
            cursos.append( cls(curso) )
        return cursos


    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM cursos WHERE id = %(id)s;"
        data = { "id": id }
        curso = connectToMySQL('db_esquema_estudantes_cursos').query_db(query, data)
        return cls(curso[0])


    @classmethod
    def save(cls, data):
        query = "INSERT INTO cursos (nome, created_at, updated_at) VALUES (%(nome)s,  NOW(), NOW())"
        return connectToMySQL('db_esquema_estudantes_cursos').query_db(query, data)


    @classmethod
    def delete(cls, id):
        query = "DELETE FROM cursos WHERE id = %(id)s;"
        data = { "id": id }
        return connectToMySQL('db_esquema_estudantes_cursos').query_db(query, data)


    @classmethod
    def update(cls, curso):
        query = "UPDATE cursos SET nome = %(nome)s, updated_at = NOW() WHERE id = %(id)s"
        data = {
            "id": curso.id,
            "nome": curso.nome,
            }
        return connectToMySQL('db_esquema_estudantes_cursos').query_db(query, data)