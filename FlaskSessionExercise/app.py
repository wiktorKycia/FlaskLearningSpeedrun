from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta
app = Flask(__name__)
app.secret_key = "abc123"
app.permanent_session_lifetime = timedelta(minutes=30)
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/home", methods=['POST','GET'])
def home():
    if request.method == "POST":
        session.permanent = True
        session['name'] = request.form['name']
        session['surname'] = request.form['surname']
        session['age'] = request.form['age']
        session['gender'] = request.form['gender']
        return redirect(url_for("home"))
    else:
        if 'name' not in session:
            return redirect(url_for("login"))
        return render_template('home.html', name=session['name'], surname=session['surname'], age=session['age'], gender=session['gender'])


@app.route("/logout")
def logout():
    session.pop('name', None)
    session.pop('surname', None)
    session.pop('age', None)
    session.pop('gender', None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
