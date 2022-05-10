from uuid import uuid4
from traceback import format_exc
from flask import Flask, render_template, request, redirect
from deta import Deta
from typing import Union
from random import choices
from string import ascii_lowercase, digits
from time import time
from os import environ

app = Flask(__name__)
deta = Deta(environ["DETA_PROJECT_KEY"])
links = deta.Base("links")
views = deta.Base("views")
errors = deta.Base("errors")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/sec_index", methods=["GET"])
def sec_index():
    return render_template("sec.html")



@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler(Exception)
def error_handler(e):
    error = errors.put(
        {"traceback": format_exc(), "time": int(time()), "key": str(uuid4())}
    )
    return render_template("error.html", error=str(e), code=error["key"])
