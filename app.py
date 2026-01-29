"""
Flask Portfolio App
Author: Spencer Renfro
Date: 2026-1-29
"""
from flask import Flask, render_template
from datetime import datetime
app = Flask(__name__)

@app.route("/")
def index():
    now = datetime.now()
    return render_template("index.html", now=now)

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name='world'):
    return render_template('hello.html', name=name)

@app.route("/polytopia")
def polytopia():
    return render_template('polytopia.html')

@app.route("/steamaction")
def steamaction():
    return render_template('steamaction.html')



