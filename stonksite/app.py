from flask import Flask, render_template, request, url_for, redirect, flash
from db import *

app = Flask(__name__)
app.secret_key = "test"

@app.route("/")
def home():
    return render_template("main.html")

if __name__ == "__main__":
    app.run()