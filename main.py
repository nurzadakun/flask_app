from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

connect = sqlite3.connect('users.db', check_same_thread=False)
cursor = connect.cursor()

@app.route("/")
def welcome():
    return render_template("index.html", name="1")

#регистрация

@app.route("/regist", methods=['GET','POST'])
def regist():
    if request.method == 'POST':
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        login = request.form['login']
        password = request.form['password']
        cursor.execute('''INSERT INTO users (login, password)
        VALUES (?, ?)
        ''', [login, password])
        connection.commit()
        connection.close()
    return render_template("regist.html")

@app.route("/auth", methods=['GET','POST'])
def auth():
    if request.method == 'POST':
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        login = request.form['login']
        password = request.form['password']

        cursor.execute('SELECT * FROM USERS WHERE login=?', [login])
        cursor.execute('SELECT * FROM USERS WHERE password=?', [password])
        user = cursor.fetchall()
        if user:
            if(user[0][2]==password):
                return render_template("welcome.html", login=login)
        connection.commit()
        connection.close()
    return render_template("auth.html")

