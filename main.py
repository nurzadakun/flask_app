from flask import Flask, render_template, request

app = Flask(__name__)

users = {'login':'password', 'nurzada':'parol'}

@app.route("/")
def welcome():
    return render_template("index.html", name="1")

@app.route("/auth", methods=['GET','POST'])
def auth():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        
        if(users[login]==password):
            return render_template("welcome.html", login=login)
    return render_template("auth.html")


