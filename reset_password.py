from flask import render_template, request, url_for, redirect
from main import app, mail
import db_context, functions
from flask_mail import Message

#запрос на изменение пароля, отправка письма на почту
@app.route("/forgot_password", methods=['GET','POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']

        user = db_context.db_context("SELECT * FROM users WHERE email = '%s'"%(email))

        if user:
            token = functions.generate_random_number()  

            
            db_context.db_context("UPDATE users SET reset_token = '%s' WHERE email = '%s'"%(token, email), commit=True)

            link = url_for('reset', token=token)
            msg = Message('Восстановление пароля', sender = 'flask_first_app', recipients = [email])
            msg.body = f"Перейдите по ссылке чтобы восстановить пароль: http://localhost:5000{link}"
            mail.send(msg)

            return render_template("auth.html")
    return render_template("forgotpassword.html")

#изменение пароля
@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset(token):
    if request.method == 'POST':
        user = db_context.db_context("SELECT * FROM users WHERE reset_token = '%s'"%(token))

        password = request.form['new_password']
        password = functions.hash_password(password)

        db_context.db_context("UPDATE users SET password = '%s', reset_token = NULL WHERE id = '%s'"%(password, user[0][0]), commit=True)
        
        return redirect("/auth")
    return render_template("resetpassword.html")