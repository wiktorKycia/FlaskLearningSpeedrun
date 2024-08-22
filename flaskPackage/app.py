from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from second import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix='/admin')
# jeśli nie damy prefixa to domyślnie będzie brało html-a z blueprinta, a nie z głównej aplikacji
# w przypadku konfliktu nazw
@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
