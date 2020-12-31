from flask import Flask, render_template, request
from flask_login import current_user
import DAO, Controller


app = Flask(__name__)
app.config['SECRET_KEY'] = "flask"
DAO.init_app(app)
Controller.init_app(app)


@app.route("/")
def log():
    return render_template("login.html")


@app.context_processor
def inject_user():
    user = current_user
    return dict(user=user)


if __name__ == '__main__':
    app.run()
