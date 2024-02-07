from FunzioniDB import *

def create_tables(connection):
    create_books = '''
    CREATE TABLE books (
    id_books INT PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    author VARCHAR(250) NOT NULL,
    year int NOT NULL
    );
'''
    create_users = '''
    CREATE TABLE users (
    id_user INT PRIMARY KEY,
    name varchar(50),
    age int
    );
'''
    create_loans = '''
    CREATE TABLE loans (
    id_loan int PRIMARY KEY AUTO_INCREMENT
    
    );
'''