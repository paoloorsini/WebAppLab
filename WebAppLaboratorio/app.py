import json
from flask import Flask, jsonify, render_template, request
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'libreria'
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

app = Flask(__name__)

@app.route('/data/books', methods=['GET'])
def get_data_books():
    query = "SELECT title FROM books"
    items = execute_query(query)
    return items

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/books')
def show_books():
    books = get_data_books()
    return render_template('books.html', books=books)

@app.route('/data/author', methods=['GET'])
def get_data_author():
    query = "SELECT author FROM books"
    items = execute_query(query)
    return items
    # return jsonify({'items': items})
@app.route('/author')
def show_author():
    author = get_data_author()
    return render_template('authors3.html', author=author)


@app.route('/data/loans', methods=['GET'])
def get_data_loans():
    query = """SELECT loans.id_loan, books.title, users.name, loans.status FROM `loans` 
            JOIN books ON books.id_books = loans.id_books
            JOIN users ON users.id_user=loans.id_user;"""
    items = execute_query(query)
    return items
@app.route('/loans')
def show_loans():
    loans = get_data_loans()
    return render_template('loans.html', loans=loans)






#singolo show in base all'id passato
@app.route('/data/shows/<int:id>', methods=['GET'])
def get_singleshows_data(id):
    query = "SELECT * FROM shows WHERE show_id = %s"
    shows = execute_query(query, (id,))
    return jsonify({'shows': shows})

@app.route('/data/books/author/<author_name>', methods=['GET'])
def get_books_by_author(author_name):
    query = """
        SELECT *
        FROM books
        WHERE author = %s
    """
    books = execute_query(query, (author_name,))
    print(books)
    return jsonify({'books': books})

# def get_books_by_author2(author_name):
#     query = """
#         SELECT *
#         FROM books
#         WHERE author = %s
#     """
#     books = execute_query(query, (author_name,))
#     print(books)
#     return books

# @app.route('/books2/author/<author_name>')
# def show_books_by_author2(author_name):
#     # Recupera tutti i libri associati all' autore specificato
#     author = get_books_by_author(author_name)
#     print(author)
#     return render_template('book_authors.html', author=author)

@app.route('/books/author/<author_name>')
def show_books_by_author(author_name):
    # Recupera tutti i libri associati all' autore specificato
    books_data_response = get_books_by_author(author_name)
    # Carica il contenuto JSON come un dizionario Python
    data = json.loads(books_data_response.get_data(as_text=True))
    # Estrai la lista di books
    author = data['books']
    return render_template('book_authors.html', author=author)

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




@app.route("/aggiungiLibro")
def aggiungi_Libro():
    return render_template("aggiungiLibro.html")

@app.route('/add/data/category', methods=['POST'])
def add_data_category():
    # Estrai i dati JSON dalla richiesta
    dati_json = request.json

    # Ottieni i valori dai dati JSON
    nome = dati_json.get('nome')
    query = "INSERT INTO categories(category_name) VALUES(%s)"
    # execute_query2(query, (nome,))
    # Restituisci una risposta

    return f"Il nome {nome} è stato aggiunto alle categorie."


if __name__ == '__main__':
    app.run(debug=True)



# aggiungere nella home page un bottone aggiungi film che se cliccato mi manda in una nuova pagina web con un form per inserire il film