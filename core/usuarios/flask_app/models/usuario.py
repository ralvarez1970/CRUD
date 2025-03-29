## Usuarios
## Roberto Alvarez, 2025

from flask_app.config.mysqlconnection import connectToMySQL

class Usuario:

    def __init__( self , data ):
        self.id = data['id']
        self.nome = data['nome']
        self.sobrenome = data['sobrenome']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL('usuarios').query_db(query)
        usuarios = []
        for usuario in results:
            usuarios.append( cls(usuario) )
        return usuarios


    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = { "id": id }
        usuario = connectToMySQL('usuarios').query_db(query, data)
        return cls(usuario[0])


    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuarios (nome, sobrenome, email, created_at, updated_at) VALUES (%(nome)s, %(sobrenome)s, %(email)s, NOW(), NOW())"
        return connectToMySQL('usuarios').query_db(query, data)


    @classmethod
    def delete(cls, id):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        data = { "id": id }
        return connectToMySQL('usuarios').query_db(query, data)


    @classmethod
    def update(cls, usuario):
        query = "UPDATE usuarios SET nome = %(nome)s, sobrenome = %(sobrenome)s, email = %(email)s WHERE id = %(id)s"
        data = {
            "id": usuario.id,
            "nome": usuario.nome,
            "sobrenome": usuario.sobrenome,
            "email": usuario.email
            }
        return connectToMySQL('usuarios').query_db(query, data)