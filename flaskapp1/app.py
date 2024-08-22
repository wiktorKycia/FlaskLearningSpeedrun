from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=24)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = True

        username = request.form['username']
        password = request.form['password']

        found_user = db.session.query(User).filter_by(username=username).first()
        if found_user and found_user.password == password:
            session['username'] = username
            session['email'] = found_user.email

            flash(f'Successfully logged in as {username}')

            return redirect(url_for('user'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    else:
        if "username" in session:
            flash("You are logged in")
            return redirect(url_for('user'))
        else:
            return render_template('login.html')

@app.route('/user')
def user():
    if 'username' in session:
        username = session['username']
        email = session['email']
        return render_template('user.html', user=username, email=email)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    flash(f'user {session["username"]} has been logged out')
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password1 = request.form['password1']

        if password != password1:
            flash('Passwords do not match')
            return redirect(url_for('register'))
        
        found_user = db.session.query(User).filter_by(username=username).first()
        if found_user:
            flash('Username already exists')
            return redirect(url_for('register'))
        
        found_user = db.session.query(User).filter_by(email=email).first()
        if found_user:
            flash('Email already exists')
            return redirect(url_for('register'))


        new_user = User(username=username, email=email, password=password)

        session['username'] = request.form['username']
        session['email'] = request.form['email']

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    else:
        if "username" in session:
            flash('You cannot register if you are already logged in')
            return redirect(url_for('user'))
        else:
            return render_template('register.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # admin = User(username='admin', password='admin123')
        # db.session.add(admin)
        # db.session.commit()
    app.run(debug=True)