from flask import Blueprint,render_template,request,session,jsonify
from market.models import db,MarketStaff
from market.utils import hash_password
user = Blueprint("user",__name__,template_folder='templates',static_folder='static')

@user.route("/login",methods=['POST'])
def log():
    jsoninput = request.get_json()
    user = MarketStaff.query\
            .filter(MarketStaff.name==jsoninput.get('name'))\
            .filter(MarketStaff.password_hash==hash_password(jsoninput.get('password')))\
            .filter(MarketStaff.delete==False).first()
    if user is not None:
        session['level'] = user.level
        session['id'] = user.id
        return jsonify({"success":True})
    else:
        return jsonify({"success":False})


@user.route('/register',methods=['POST'])
def reg():
    jsoninput = request.get_json()
    _u = MarketStaff()
    return '1'