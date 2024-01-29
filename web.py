from flask import Flask, render_template
import pymysql

app = Flask(__name__)

# Configuration de la base de données MariaDB
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'votre_utilisateur',
    'password': 'votre_mot_de_passe',
    'database': 'votre_base_de_donnees',
}

def connect_db():
    return pymysql.connect(**DATABASE_CONFIG)

@app.route('/')
def index():
    # Récupérer les données de la base de données
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM votre_table')
    data = cursor.fetchall()
    conn.close()

    # Passer les données à la page web (utilisation de Jinja2 pour afficher les données)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
