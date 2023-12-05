import pyodbc
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)
app.config["SECRET_KEY"] = "emyeucoquyen"

@app.route("/")
def route_index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
