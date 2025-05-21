from flask_app.config.mysqlconnection import connectToMySQL

class Usuario:
    db = "usuarios_ajax"
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def guardar(cls,data):
        query  = "INSERT INTO usuarios (nombre, email) VALUES (%(nombre)s,%(email)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def obtener_por_nombre(cls,data):
        query = "SELECT * FROM usuarios WHERE nombre = %(nombre)s;"
        resultados = connectToMySQL(cls.db).query_db(query,data)
        if not resultados:
            return False
        return cls(resultados[0])

    @classmethod
    def ver_todos_json(cls):
        query = "SELECT * FROM usuarios;"
        resultados = connectToMySQL(cls.db).query_db(query)
        usuarios = []
        for datos_usuario in resultados:
            usuarios.append( datos_usuario )
        return usuarios