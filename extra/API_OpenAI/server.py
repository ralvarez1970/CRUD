from flask_app import app
import os

if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG"), port=os.getenv("PORT"))