"""
#这是一个测试demo
a=[1,3,5,7,8]
b=3
print("******1******")
assert b in a,'False'
assert b not in a, 'False'
"""
from flask import Blueprint ,render_template
supplyer = Blueprint("supplyer",__name__,template_folder='templates',static_folder='static')

@supplyer.route("/supplyer/")
def manage_supplyer():
    return render_template('supplyer.html')

@supplyer.route("/supplyer/Add/")
def supplyer_add():
    return render_template('supplyerAdd.html')

@supplyer.route("/supplyer/Modify/")
def supplyer_modify():
    return render_template('supplyerModify.html')
    