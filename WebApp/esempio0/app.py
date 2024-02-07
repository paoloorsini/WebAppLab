from flask import Flask,jsonify

app = Flask(__name__)

@app.route("/test")
def homepage():
    return "Hello World!"

@app.route("/contatti")
def contatti():
    lista_nomi=["marco","mario","giovanna"]
    return jsonify({"contatti":lista_nomi})

if __name__ == '__main__':
    app.run(debug=True)