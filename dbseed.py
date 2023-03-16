import sqlite3


connection=sqlite3.connect('users.db')

cursor= connection.cursor()

cursor.execute('drop table users')

cursor.execute('''
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL
) 
''')
connection.commit()
