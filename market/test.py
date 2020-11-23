from flask import Blueprint
tests = Blueprint("test",__name__)

@tests.route("/hello")
def helo():
    return "world"