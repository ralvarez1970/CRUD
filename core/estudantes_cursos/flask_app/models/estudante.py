## Estudantes & cursos
## Roberto Alvarez, 2025

from flask_app.config.mysqlconnection import connectToMySQL

class Estudante:

    def __init__( self , data):
        self.id = data['id']
        self.nome = data['nome']
        self.sobrenome = data['sobrenome']
        self.email = data['email']
        self.idade = data['idade']
        self.curso_id = data['curso_id']
        self.curso = data['curso']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    @classmethod
    def get_all(cls):
        query = """
        SELECT estudantes.id as id, estudantes.nome as nome, estudantes.sobrenome as sobrenome, estudantes.email as email, estudantes.idade as idade, estudantes.created_at as created_at, estudantes.updated_at as updated_at, estudantes.curso_id as curso_id, cursos.nome as curso 
        FROM estudantes
        LEFT JOIN cursos
        ON estudantes.curso_id = cursos.id;"""

        results = connectToMySQL('db_esquema_estudantes_cursos').query_db(query)
        estudantes = []
        for estudante in results:
            print (estudante)
            estudantes.append( cls(estudante) )
        return estudantes


    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM estudantes WHERE id = %(id)s;"
        data = { "id": id }
        estudante = connectToMySQL('db_esquema_estudantes_cursos').query_db(query, data)
        return cls(estudante[0])


    @classmethod
    def select(cls, curso_id):
        query = "SELECT * FROM estudantes WHERE curso_id = %(id)s;"
        data = { "id": curso_id }
        results = connectToMySQL('db_esquema_estudantes_cursos').query_db(query, data)
        estudantes = []
        for estudante in results:
            estudante['curso'] = ''
            estudantes.append( cls(estudante) )
        return estudantes


    @classmethod
    def save(cls, data):
        query = "INSERT INTO estudantes (nome, sobrenome, email, idade, created_at, updated_at, curso_id) VALUES (%(nome)s, %(sobrenome)s, %(email)s, %(idade)s, NOW(), NOW(), %(curso_id)s)"
        return connectToMySQL('db_esquema_estudantes_cursos').query_db(query, data)


    @classmethod
    def delete(cls, id):
        query = "DELETE FROM estudantes WHERE id = %(id)s;"
        data = { "id": id }
        return connectToMySQL('db_esquema_estudantes_cursos').query_db(query, data)


    @classmethod
    def update(cls, estudante):
        query = "UPDATE estudantes SET nome = %(nome)s, sobrenome = %(sobrenome)s, email = %(email)s, idade = %(idade)s, updated_at = NOW(), curso_id = %(curso_id)s WHERE id = %(id)s"
        data = {
            "id": estudante.id,
            "nome": estudante.nome,
            "sobrenome": estudante.sobrenome,
            "email": estudante.email,
            "idade": estudante.idade,
            "curso_id": estudante.curso_id,
            }
        return connectToMySQL('db_esquema_estudantes_cursos').query_db(query, data)