import requests
# https://www.w3schools.com/python/ref_requests_response.asp

# Esempio di URL per una richiesta GET
url = "http://127.0.0.1:5000/contatti"

# Fare la richiesta GET
response = requests.get(url)
print(type(response))

# Verifica se la richiesta ha avuto successo (status code 200)
if response.status_code == 200:
    # Se la richiesta ha avuto successo, ottieni il contenuto della risposta come JSON
    data = response.json()
    # Stampare i dati ottenuti
    print(data)
#     print(response.json())
else:
    # Se la richiesta non ha avuto successo, stampa un messaggio di errore
    print("Errore durante la richiesta:", response.status_code)