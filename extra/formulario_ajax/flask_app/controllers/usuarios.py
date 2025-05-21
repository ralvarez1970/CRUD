from flask_app.models.usuario import Usuario
from flask_app import app
from flask import render_template, jsonify, request, redirect

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/usuarios')
def usuarios():
    return jsonify(Usuario.ver_todos_json())

@app.route('/crear/usuario',methods=['POST'])
def crear_usuario():
    
    pass



