from market.views.manage import manage
from flask import render_template,g,jsonify,redirect,url_for,request
from market.models import db,MarketSupplyer
from faker import Faker
f=Faker(locale='zh_CN')
@manage.route("/supplyerinfo",methods=['GET','POST','PUT'])
def supplyer_home():
    if request.method=='GET':
        suppliers = MarketSupplyer.query.all()
        result = []
        for s in suppliers:
            result.append(s.todict())
        return jsonify(result)
    elif request.method=='POST':
        _m = MarketSupplyer(
            supplyer_id=request.form.get('supplyerid'),
            name=request.form.get('supplyername'),
            name_short=request.form.get('supplyerabbr'),
            address=request.form.get('supplyeraddress'),
            telephone=request.form.get('supplyerphone'),
            email=request.form.get('supplyeremail'),
            contact=request.form.get('supplyerperson'),
            contact_phone=request.form.get('supplyerperson-phone'),
            comment=request.form.get('supplyerremarks'),
        )
        db.session.add(_m)
        try:
            db.session.commit()
            return jsonify({"success":True})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"success":False})
@manage.route('/test')
def test():
    return render_template('test.html',title='bruh')

@manage.route('/supplyer')
def manage_supplyer():
    return render_template('supplyer.html') 

@manage.route('/supplyerpopulate')
def populate_sup():
    for i in range(5):
        _m = MarketSupplyer(
            supplyer_id=f.ssn(),
            name = f.first_name(),
            name_short = f.last_name(),
            address = f.address(),
            telephone = f.phone_number(),
            email = f.email(),
            contact= f.phonenumber_prefix(),
            contact_phone = f.phone_number(),
        )
        db.session.add(_m)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    return redirect(url_for('manage.manage_home'))