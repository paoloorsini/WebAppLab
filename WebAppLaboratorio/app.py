import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
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

def execute_query_insert(query, params=None):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'il_tuo_valore_segreto'

@app.route('/')
def home():
    return render_template('home2.html')


@app.route('/data/books', methods=['GET'])
def get_data_books():
    query = "SELECT title FROM books"
    items = execute_query(query)
    return items


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


@app.route('/add/data_book', methods=['POST'])
def add_data_book():
    content_type = request.headers.get('Content-Type')

    if content_type == 'application/json':
        data = request.json
        title = data.get('title')
        author = data.get('author')
        year = data.get('year')
    elif content_type == 'application/x-www-form-urlencoded':
        data = request.form
        title = data['title']
        author = data['author']
        year = data['year']
    else:
        return jsonify({'error': 'Unsupported Content-Type'}), 415
    query = "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)"
    values = (title, author, year)
    execute_query_insert(query, values)

    flash(f"Il libro {title} di {author} è stato aggiunto alla libreria.")
    return redirect(url_for('home'))

@app.route('/addbook')
def add_book():
    return render_template("addbook.html")

@app.route('/addloan', methods=['GET'])
def add_loan():
    return render_template("addloan.html")

@app.route('/add/data/loans', methods=['POST'])
def add_data_loan():
    try:
        if request.json:
            dati_json = request.json
            libro_id = dati_json.get('id_books')
            utente_id = dati_json.get('id_user')
            status = dati_json.get('status')
        elif request.form:
            form_data = request.form
            libro_id = form_data['id_books']
            utente_id = form_data['id_user']
            status = form_data['status']

        if libro_id is None or utente_id is None:
            raise ValueError("I dati non sono validi")

        query = "INSERT INTO loans (id_books, id_user, status) VALUES (%s, %s, %s)"
        values = (libro_id, utente_id, status)
        execute_query_insert(query, values)

        return jsonify({"message": "Prestito inserito con successo"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)



