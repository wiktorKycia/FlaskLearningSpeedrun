from flask import Blueprint, render_template

second = Blueprint('second', __name__, static_folder='static', template_folder='templates')
# można mieć inne foldery static i templates


@second.route('/home')
@second.route('/')
def home():
    return render_template("home.html")
