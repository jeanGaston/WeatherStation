import mysql.connector
from mysql.connector import Error

def create_database_if_not_exists(host, user, password, database):
    try:
        # Connexion au serveur MySQL sans spécifier de base de données
        conn = mysql.connector.connect(host=host, user=user, password=password)

        # Création du curseur
        cursor = conn.cursor()

        # Vérification si la base de données existe déjà
        cursor.execute("SHOW DATABASES LIKE %s", (database,))
        database_exists = cursor.fetchone()

        if not database_exists:
            # Si la base de données n'existe pas, création
            cursor.execute("CREATE DATABASE {}".format(database))
            print("Base de données créée avec succès")
        else:
            print("La base de données existe déjà")

    except Error as e:
        print("Erreur lors de la connexion à MySQL :", e)

    finally:
        # Fermeture du curseur et de la connexion
        if conn.is_connected():
            cursor.close()
            conn.close()

def create_table_if_not_exists(host, user, password, database):
    try:
        # Connexion à la base de données spécifiée
        conn = mysql.connector.connect(host=host, user=user, password=password, database=database)

        # Création du curseur
        cursor = conn.cursor()

        # Définition de la requête de création de table si elle n'existe pas
        create_table_query = """
        CREATE TABLE IF NOT EXISTS mes_mesures (
            id INT AUTO_INCREMENT PRIMARY KEY,
            temperature FLOAT,
            taux_humidite FLOAT,
            time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        # Exécution de la requête
        cursor.execute(create_table_query)
        print("Table créée avec succès ou déjà existante")

    except Error as e:
        print("Erreur lors de la création de la table :", e)

    finally:
        # Fermeture du curseur et de la connexion
        if conn.is_connected():
            cursor.close()
            conn.close()

def main():
    # Paramètres de connexion à MySQL
    host = "localhost"
    user = "votre_utilisateur"
    password = "votre_mot_de_passe"
    database = "votre_base_de_donnees"

    create_database_if_not_exists(host, user, password, database)
    create_table_if_not_exists(host, user, password, database)

if __name__ == "__main__":
    main()
