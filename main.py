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
        login = request.form['login']
        password = request.form['password']

        cursor.execute('''INSERT INTO users (login, password)
        VALUES (?, ?)
        ''', [login, password])
    return render_template("regist.html")


@app.route("/auth", methods=['GET','POST'])
def auth():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        cursor.execute('SELECT * FROM USERS WHERE login=?', [login])
        user = cursor.fetchall()
        
        if(user[0][1]==password):
            return render_template("welcome.html", login=login)
    return render_template("auth.html")
