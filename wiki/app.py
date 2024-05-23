import os
from flask import Flask, render_template, Blueprint

web_ui = Blueprint("web_ui", __name__, url_prefix="/")

def create_app():
    """
    Crée et configure l'application Flask principale.

    Returns:
        Flask: L'application Flask créée et configurée.
    """
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.register_blueprint(web_ui)
    app.static_folder = 'templates'
    return app

@web_ui.route('/home', methods=['GET', 'POST'])
def home():
    """Affiche la page web principale avec la liste de toutes les tâches.

    Returns:
        Flask.Response: La page HTML contenant la liste de toutes les tâches.
    """
    return render_template("accueil.html")

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
