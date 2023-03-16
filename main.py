from flask import Flask, render_template, request
import sqlite3
import hashlib

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("index.html", name="1")

#регистрация

@app.route("/regist", methods=['GET','POST'])
def regist():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        email = request.form['email']

        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()

        cursor.execute('''INSERT INTO users (login, email, password)
        VALUES (?, ?, ?)
        ''', [login, password, email])

        connect.commit()
        connect.close()
    return render_template("regist.html")

def hash_password(password):
    password = hashlib.sha256(password)
    return password


@app.route("/auth", methods=['GET','POST'])
def auth():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()

        cursor.execute('SELECT * FROM USERS WHERE login=?', [login])
        cursor.execute('SELECT * FROM USERS WHERE password=?', [password])
        user = cursor.fetchall()

        if user:
            if(user[0][3]==password):
                return render_template("welcome.html", login=login)
            
        connect.commit()
        connect.close()
    return render_template("auth.html")

