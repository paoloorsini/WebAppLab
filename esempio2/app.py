import json
import mysql.connector

from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Configura la connessione al database MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'DB_test_Netflix'
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


@app.route("/")
def homepage():
    return render_template("home.html")


@app.route("/contatti")
def contatti():
    lista_nomi = ["marco", "mario", "giovanna"]
    # json_data = json.dumps(lista_nomi)
    return jsonify({"contatti": lista_nomi})

@app.route("/api/movies/all")
def data_movies_all():
    query = """ SELECT * FROM shows """
    items = execute_query(query)
    return items

@app.route("/api/movies/movie")
def data_movies_movie():
    query = """ SELECT * FROM shows WHERE type = 'Movie' """
    items = execute_query(query)
    return items

@app.route("/api/movies/series")
def data_movies_series():
    query = """ SELECT * FROM shows WHERE type = 'TV Show' """
    items = execute_query(query)
    return items

@app.route("/api/moviesq/<tipo>")
def data_movies(tipo):
    query = """ SELECT * FROM shows WHERE type = %s """
    items = execute_query(query, (tipo,))
    return items

@app.route("/api/movie/<id>")
def data_movie_id(id):
    query = """ SELECT * FROM shows WHERE show_id = %s """
    items = execute_query(query, (id,))
    return items

@app.route("/api/generi")
def generi():
    lista_generi = [
        {
            "id": 1,
            "titolo": "horror"
        },
        {
            "id": 2,
            "titolo": "avventura"
        },
        {
            "id": 3,
            "titolo": "politico"
        }
    ]
    return jsonify(lista_generi)


@app.route("/movies")
def movies():
    data = data_movies_all()
    #print(data)
    print(type(data))

    return render_template("movies.html",lista_film=data)

@app.route("/show")
def movies_show():
    data = data_movies_series()
    #print(data)
    print(type(data))

    return render_template("movies.html",lista_film=data)

@app.route("/movie")
def movies_movie():
    data = data_movies_movie()
    #print(data)
    print(type(data))

    return render_template("movies.html",lista_film=data)

# @app.route("/movies")
# def movies():
#     import requests
#     url = "http://127.0.0.1:5000/api/movies"
#
#     response = requests.get(url)
#     print(type(response))
#     data = response.json()
#     lista_film = data["films"]
#     print(lista_film)
#
#     return render_template("movies.html")


if __name__ == '__main__':
    app.run(debug=True)
