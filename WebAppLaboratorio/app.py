import json

from flask import Flask, jsonify, render_template, request
import mysql.connector

app = Flask(__name__)

# Configura la connessione al database MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'testdb'
}

# Funzione per creare una connessione al database
def create_db_connection():
    return mysql.connector.connect(**db_config)

# Funzione per eseguire query SQL
def execute_query(query, params=None):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def execute_query2(query, params=None):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    cursor.close()
    connection.close()


# Rotte dell'API
@app.route('/data/categories', methods=['GET'])
def get_data_categories():
    query = "SELECT * FROM categories"
    items = execute_query(query)
    return items
    # return jsonify({'items': items})

@app.route('/data/shows', methods=['GET'])
def get_data_shows():
    query = "SELECT * FROM shows"
    items = execute_query(query)
    return items

#singolo show in base all'id passato
@app.route('/data/shows/<int:id>', methods=['GET'])
def get_singleshows_data(id):
    query = "SELECT * FROM shows WHERE show_id = %s"
    shows = execute_query(query, (id,))
    return jsonify({'shows': shows})

@app.route('/data/shows/category/<category_name>', methods=['GET'])
def get_shows_by_category(category_name):
    query = """
        SELECT s.*
        FROM shows s
        JOIN showcategories sc ON s.show_id = sc.show_id
        JOIN categories c ON sc.category_id = c.category_id
        WHERE c.category_name = %s
    """
    shows = execute_query(query, (category_name,))
    return jsonify({'shows': shows})

@app.route('/data/shows/category/id/<category_id>', methods=['GET'])
def get_shows_by_category_id(category_id):
    query = """
        SELECT s.*
        FROM shows s
        JOIN showcategories sc ON s.show_id = sc.show_id
        JOIN categories c ON sc.category_id = c.category_id
        WHERE c.category_id = %s
    """
    shows = execute_query(query, (category_id,))
    return jsonify({'shows': shows})
    # return shows

@app.route('/movies')
def show_movies():
    movies = get_data_shows()
    return render_template('movies.html', movies=movies)

@app.route('/categories')
def show_categories():
    categories = get_data_categories()
    return render_template('categories.html', categories=categories)

@app.route('/movies/category/<int:category_id>')
def show_movies_by_category(category_id):
    # Recupera tutti i film associati alla categoria specificata
    shows_data_response = get_shows_by_category_id(category_id)
    # Carica il contenuto JSON come un dizionario Python
    data = json.loads(shows_data_response.get_data(as_text=True))

    # Estrai la lista di show
    movies = data['shows']
    return render_template('movie_by_category.html', movies=movies)

# Funzione per ottenere il nome della categoria
def get_category_name(category_id):

    pass



@app.route('/')
def home():
    return render_template('home.html')

@app.route("/aggiungiFilm")
def aggiungi_film():
    return render_template("aggiungiFilm.html")

@app.route('/add/data/category', methods=['POST'])
def add_data_category():
    # Estrai i dati JSON dalla richiesta
    dati_json = request.json

    # Ottieni i valori dai dati JSON
    nome = dati_json.get('nome')
    query = "INSERT INTO categories(category_name) VALUES(%s)"
    execute_query2(query, (nome,))
    # Restituisci una risposta
    return f"Il nome {nome} è stato aggiunto alle categorie."


if __name__ == '__main__':
    app.run(debug=True)

# aggiungere nella home page un bottone aggiungi film che se cliccato mi manda in una nuova pagina web con un form per inserire il film