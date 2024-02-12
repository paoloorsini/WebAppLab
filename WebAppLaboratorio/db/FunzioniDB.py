import mysql.connector
from mysql.connector import Error
import csv

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def creaDB(connection, name):
    create_database(connection, f"CREATE DATABASE %s" % name)

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print("Query successful")
    except Error as err:
        print(query, f"Error: '{err}'")


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def read_query_place(connection, query, place):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, place)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def execute_many(connection, query, sequence):
    cursor = connection.cursor()
    try:
        cursor.executemany(query, sequence)
        connection.commit()
        print("Execute many successful")
    except Error as err:
        print(f"Error: '{err}'")


def execute_query_place(connection, query, place):
    cursor = connection.cursor()
    try:
        cursor.execute(query, place)
        connection.commit()
        # print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
        print(query)


def inserisci_dati_utente(connection,pw,db):
    with open("utenti.csv", "r", encoding="utf_8") as f:
        lettore = csv.reader(f)
        next(lettore)
        lettore = list(lettore)
        for elem in lettore:
            q = """INSERT INTO users(name, age) VALUES(%s,%s);"""
            place = (elem[0], elem[1])
            execute_query_place(connection, q, place)


def inserisci_dati_libri(connection,pw,db):
    with open("libri.csv", "r", encoding="utf_8") as f:
        lettore = csv.reader(f)
        next(lettore)
        lettore = list(lettore)
        for elem in lettore:
            q = """INSERT INTO books(title,author,year) VALUES(%s,%s,%s);"""
            place = (elem[0], elem[1], elem[2])
            execute_query_place(connection, q, place)

def inserisci_dati_prestiti(connection,pw,db):
    with open("prestiti.csv", "r", encoding="utf_8") as f:
        lettore = csv.reader(f)
        next(lettore)
        lettore = list(lettore)
        for elem in lettore:
            q = """INSERT INTO loans(id_books, id_user, status) VALUES(%s,%s,%s);"""
            place = (elem[2], elem[1], elem[3])
            execute_query_place(connection, q, place)
