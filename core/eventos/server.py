## Coding Dojo - Python Bootcamp Jan 2025
## Eventos
## Roberto Alvarez, 2025

from flask_app import app

from flask_app.controllers import usuarios
from flask_app.controllers import eventos
from flask_app.controllers import autenticacao

if __name__ == "__main__":
    
    app.run(debug=True)