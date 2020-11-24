from flask import Blueprint,render_template,request,session,jsonify,url_for
from market.models import db,MarketStaff
from market.utils import hash_password
user = Blueprint("user",__name__,template_folder='templates',static_folder='static')

@user.route("/login",methods=['POST'])
def log():
    jsoninput = request.get_json()
    user = MarketStaff.query\
            .filter(MarketStaff.telephone==jsoninput.get('telephone'))\
            .filter(MarketStaff.password_hash==hash_password(jsoninput.get('password')))\
            .filter(MarketStaff.delete==False).first()
    if user is not None:
        session['level'] = user.level
        session['id'] = user.id
        if user.level != 'admin':
            return jsonify({"success":True,"data":"登录成功","redirect":url_for('browse.browse_home')})
        else:
            return jsonify({"success":True,"data":"登录成功","redirect":url_for('manage.manage_home')})
    else:
        return jsonify({"success":False,"details":"用户名或密码错误"})


@user.route('/register',methods=['POST'])
def reg():
    jsoninput = request.get_json()
    _u = MarketStaff(
        name = jsoninput.get('name'),
        password_hash = hash_password(jsoninput.get('password')),
        telephone = jsoninput.get('telephone'),
        salary = jsoninput.get('salary'),
    )
    db.session.add(_u)
    try:
        db.session.commit()
        return jsonify({"success":True,"data":"注册成功"})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"success":False,"details":"该电话号码已存在"})
    