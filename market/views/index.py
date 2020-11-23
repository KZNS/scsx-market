from flask import Blueprint,render_template
index = Blueprint("index",__name__,template_folder='templates',static_folder='static')

@index.route("/")
def helo():
    return render_template('index.html')