#все что связано со входом, регистрацией и выходом 

from flask import render_template, request, redirect, session
from main import app
import functions, db_context


#регистрация
@app.route("/regist", methods=['GET','POST'])
def regist():
    if request.method == 'POST':
        email = request.form['email']
        login = request.form['login']
        password = request.form['password']

        password = functions.hash_password(password)

        db_context.db_context('''INSERT INTO users (login, email, password)
        VALUES ('%s', '%s', '%s')
        '''%(login, email, password), commit=True)

    return render_template("regist.html")

#авторизация
@app.route("/auth", methods=['GET','POST'])
def auth():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        password = functions.hash_password(password)

        user = db_context.db_context("SELECT * FROM USERS WHERE login='%s' AND password='%s'"%(login, password))
        if user:
            if(user[0][3]==password):
                session["name"] = login
                session["user_id"] = user[0][0]
                return redirect("/")
            
    return render_template("auth.html")

#выход
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")