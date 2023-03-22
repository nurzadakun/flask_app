from flask import render_template, request
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

