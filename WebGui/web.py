from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# ... (configuration de la base de données)
db_config = {
    'host': 'localhost',
    'user': 'votre_utilisateur',
    'password': 'votre_mot_de_passe',
    'database': 'ma_base_de_donnees',
}

# Route pour afficher les données depuis la base de données
@app.route('/')
def afficher_donnees():
    try:
        # Connexion à la base de données
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Exécution de la requête pour récupérer les données
        query = "SELECT colonne1, colonne2 FROM ma_table"
        cursor.execute(query)

        # Récupération des résultats
        resultats = cursor.fetchall()

        # Fermeture des connexions
        cursor.close()
        connection.close()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Si la requête est une demande AJAX, renvoyer uniquement le contenu du tableau
            return render_template('tableau_donnees.html', resultats=resultats)
        else:
            # Sinon, renvoyer la page complète
            return render_template('index.html', resultats=resultats)

    except Exception as e:
        return f"Erreur : {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
