from Tables import *
import csv
from FunzioniDB import *

host = 'localhost'
user = 'root'
password = ''
database = 'libreria'

create_server_connection(host, user, password)
connection = create_db_connection(host, user, password, database)
# create_tables(connection)
inserisci_dati_utente(connection,password,database)
inserisci_dati_libri(connection,password,database)
inserisci_dati_prestiti(connection,password,database)