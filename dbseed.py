import sqlite3


connection=sqlite3.connect('users.db')
cursor= connection.cursor()

#cursor.execute('drop table users')
#cursor.execute('''
#CREATE TABLE users(
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    login VARCHAR(50) NOT NULL UNIQUE,
#    email VARCHAR(50) NOT NULL UNIQUE,
#    password VARCHAR(50) NOT NULL,
#    reset_token TEXT DEFAULT NULL
#)''')

cursor.execute('''
CREATE TABLE messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id_sender INTEGER,
    user_id_receiver INTEGER,
    message_text TEXT,
    message_datetime DATETIME,
    FOREIGN KEY (user_id_sender) REFERENCES users (id),
    FOREIGN KEY (user_id_receiver) REFERENCES users (id)
)''')
connection.commit()
connection.close()
