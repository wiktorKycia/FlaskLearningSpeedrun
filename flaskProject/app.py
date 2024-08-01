from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route('/')
def home():  # put application's code here
    # return render_template('list.html', names=["Donald", "Andrew", "Joe", "Barack", "Kamala"])
    return render_template("index.html")

@app.route('/test')
def test():  # put application's code here
    # return render_template('list.html', names=["Donald", "Andrew", "Joe", "Barack", "Kamala"])
    # return render_template("index.html")
    return render_template("test.html", heading="test page")

# @app.route('/<name>')
# def user(name):
#     return f"Hello {name}!"
#
# @app.route("/admin/")
# def admin():
#     return redirect(url_for("user", name="Admin!")) # <- tu podajemy nazwę do funkcji reprezentującej stronę

if __name__ == '__main__':
    app.run(debug=True)
