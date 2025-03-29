from flask import Flask, render_template, request, redirect, url_for

# Importamos la clase de mascota.py

from mascota import Mascota

app = Flask(__name__)

@app.route("/")
def index():
    # Invocamos al método de clase get all para obtener todas las mascotas
    mascotas = Mascota.get_all()
    print(mascotas)
    return render_template("index.html", todas_mascotas = mascotas)


@app.route("/entra_mascota", methods=['POST'])
def entra_mascota():
    dados = {
        "nombre": request.form['nome'],
        "tipo": request.form['tipo'],
        "color": request.form['cor']
    }
    print("Dados enviados:", dados) 
    Mascota.save(dados)
    print("Bichinho incluido")
    return redirect ('/')


@app.route("/elimina_mascota", methods=['POST'])
def elimina_mascota():
    id = (request.form['id_mascota'])
    Mascota.delete(id)
    return redirect ('/')


@app.route("/get_data_mascota", methods=['POST'])
def get_data_mascota():
    id = int(request.form['id_mascota'])
    registro = Mascota.get_one(id)
    return redirect ( url_for ("editar_mascota", nombre = registro.nombre, tipo = registro.tipo, color = registro.color, id = id))
    

@app.route("/editar_mascota")
def editar_mascota():
    id = request.args.get("id")
    nombre = request.args.get('nombre')
    tipo = request.args.get('tipo')
    color = request.args.get('color')
    return render_template("editar.html", nombre = nombre, tipo = tipo, color = color, id = id)


@app.route("/update_mascota", methods=['POST'])
def update_mascota():
    id = int(request.form['id_mascota'])
    mascota = Mascota.get_one(id)
    mascota.nombre = request.form['nome'] 
    mascota.tipo = request.form['tipo'] 
    mascota.color = request.form['cor'] 
    Mascota.atualiza(mascota)
    return redirect ('/')

if __name__ == "__main__":
    app.run(debug=True)