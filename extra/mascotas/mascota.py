# Importamos la función que devolverá una instancia de una conexión

from mysqlconnection import connectToMySQL

# Creamos la clase basada en la tabla de mascotas

class Mascota:

    def __init__( self , data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.tipo = data['tipo']
        self.color = data['color']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # Criamos un método de clase para consultar nuestra base de datos


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM mascotas;"
        # Llamamos a función connectToMySQL con el esquema al que te diriges
        resultados = connectToMySQL('primera_app_mysql').query_db(query)
        # Creamos una lista vacía para agregar nuestras instancias de mascota
        mascotas = []
        # Iteramos sobre los resultados de la base de datos y crear instancias de mascota con cls
        for mascota in resultados:
            mascotas.append( cls(mascota) )
        return mascotas
    

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM mascotas WHERE id = %(id)s;"
        dados = { "id": id }
        mascota = connectToMySQL('primera_app_mysql').query_db(query, dados)
        return cls(mascota[0])


    @classmethod
    def save(cls, dados):
        query = "INSERT INTO mascotas (nombre, tipo, color, created_at, updated_at) VALUES (%(nombre)s, %(tipo)s, %(color)s, NOW(), NOW())"
        return connectToMySQL('primera_app_mysql').query_db(query, dados)
    

    @classmethod
    def delete(cls, id):
        dados = { "id": id }
        query = "DELETE FROM mascotas WHERE id = %(id)s;"
        return connectToMySQL('primera_app_mysql').query_db(query, dados)
    

    @classmethod
    def atualiza(cls, dados):
        data = {
            "nombre": dados.nombre,
            "tipo": dados.tipo,
            "color": dados.color,
            "id": dados.id
            }
        query = "UPDATE mascotas SET nombre = %(nombre)s, tipo = %(tipo)s, color = %(color)s WHERE id = %(id)s"
        return connectToMySQL('primera_app_mysql').query_db(query, data)