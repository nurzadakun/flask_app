from flask import Flask, render_template, request, url_for, redirect
import sqlite3
import hashlib
import random
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'nurzada670@gmail.com'
app.config['MAIL_PASSWORD'] = 'wxtcbdbyciknjgqt'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

connect = sqlite3.connect('users.db', check_same_thread=False)
cursor = connect.cursor()

@app.route("/")
def welcome():
    return render_template("index.html")

#регистрация

@app.route("/regist", methods=['GET','POST'])
def regist():
    if request.method == 'POST':
        email = request.form['email']
        login = request.form['login']
        password = request.form['password']

        password = hash_password(password)

        cursor.execute('''INSERT INTO users (login, email, password)
        VALUES ('%s', '%s', '%s')
        '''%(login, email, password))

        connect.commit()
        connect.close()
    return render_template("regist.html")

#зашифровка пароля
def hash_password(password):
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return password

#авторизация
@app.route("/auth", methods=['GET','POST'])
def auth():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        password = hash_password(password)

        cursor.execute("SELECT * FROM USERS WHERE login='%s' AND password='%s'"%(login, password))
        user = cursor.fetchall()
        connect.commit()
        connect.close()
        if user:
            if(user[0][3]==password):
                return render_template("index.html", login=login)
            
        
    return render_template("auth.html")

#создание рандомного числа 
def generate_random_number():
    number = random.randint(10000, 99999)
    return number

#запрос на изменение пароля, отправка письма на почту
@app.route("/forgot_password", methods=['GET','POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']

        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM users WHERE email = '%s'"%(email))
        user = cursor.fetchone()

        if user:
            token = generate_random_number()  

            connect = sqlite3.connect('users.db')
            cursor = connect.cursor()
            cursor.execute("UPDATE users SET reset_token = '%s' WHERE email = '%s'"%(token, email))

            link = url_for('reset', token=token)
            msg = Message('Восстановление пароля', sender = 'flask_first_app', recipients = [email])
            msg.body = f"Перейдите по ссылке чтобы восстановить пароль: http://localhost:5000{link}"
            mail.send(msg)

            connect.commit()
            connect.close()
            return render_template("auth.html")
        connect.commit()
        connect.close()
    return render_template("forgotpassword.html")

#изменение пароля
@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset(token):
    if request.method == 'POST':
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM users WHERE reset_token = '%s'"%(token))
        user = cursor.fetchone()

        password = request.form['new_password']
        password = hash_password(password)

        cursor.execute("UPDATE users SET password = '%s', reset_token = NULL WHERE id = '%s'"%(password, user[0]))
        
        connect.commit()
        connect.close()

        return redirect("/auth")
    return render_template("resetpassword.html")

