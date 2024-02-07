import json

from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("home.html")


@app.route("/contatti")
def contatti():
    lista_nomi = ["marco", "mario", "giovanna"]
    # json_data = json.dumps(lista_nomi)
    return jsonify({"contatti": lista_nomi})


@app.route("/api/movies")
def data_movies():
    lista_film = [
        {
            "id": 1,
            "titolo": "Il padrino",
            "anno": 1972
        },
        {
            "id": 2,
            "titolo": "Forrest Gump",
            "anno": 1994
        },
        {
            "id": 3,
            "titolo": "La vita è bella",
            "anno": 1997
        },
        {
            "id": 4,
            "titolo": "interstellar",
            "anno": 2007
        }
    ]
    # lista_film = json.dumps(lista_film)
    return jsonify({"films":lista_film})
    # return lista_film


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
    data = data_movies()
    print(type(data))
    lista_film=data.json["films"]
# ESTRAIAMO DALLA RESPONSE LA RISPOSTA JSON ALLA CHIAVE FILMS CHE CONTIENE L'EFFETTIVA LISTA DI DIZIONARIO
    print(lista_film)
    return render_template("movies.html",lista_film=lista_film)

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
