from FunzioniDB import *

def create_tables(connection):
    create_books = '''
    CREATE TABLE books (
    id_books INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(250) NOT NULL,
    author VARCHAR(250) NOT NULL,
    year int NOT NULL
    );
'''
    create_users = '''
    CREATE TABLE users (
    id_user INT PRIMARY KEY AUTO_INCREMENT,
    name varchar(50),
    age int
    );
'''
    create_loans = '''
    CREATE TABLE loans (
    id_loan int PRIMARY KEY AUTO_INCREMENT,
    id_books INT,
    id_user INT,
    status VARCHAR(250) NOT NULL
    );
'''
    alter_loans = '''
    ALTER TABLE loans
    ADD FOREIGN KEY (id_books) REFERENCES books(id_books) ON DELETE CASCADE ON UPDATE CASCADE,
    ADD FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE CASCADE ON UPDATE CASCADE;
'''

    execute_query(connection, create_books)
    execute_query(connection, create_users)
    execute_query(connection, create_loans)
    execute_query(connection, alter_loans)