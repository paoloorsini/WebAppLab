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