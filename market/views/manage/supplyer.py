from market.views.manage import manage
from flask import render_template,g,jsonify,redirect,url_for,request,abort
from market.models import db,MarketSupplyer
from faker import Faker
f=Faker(locale='zh_CN')
@manage.route("/supplyerinfo",methods=['GET','POST','PUT','DELETE'])
def supplyer_home():
    if request.method=='GET':
        #### START FUZZY SEARCH ####
        args_dict = dict(request.values)
        query_dict = {}
        for k in args_dict:
            if args_dict[k]!='' and hasattr(MarketSupplyer,k):
                query_dict[k]=args_dict[k]

        data = MarketSupplyer.query.filter(MarketSupplyer.delete!=True)
        for k in query_dict:
            data = data.filter(getattr(MarketSupplyer,k).like('%%'+query_dict[k]+'%%'))
        suppliers = data.all()
        #### END OF FUZZY SEARCH ####
        result = []
        for s in suppliers:
            result.append(s.todict())
        return jsonify(result)
    elif request.method=='POST':
        if request.form.get('hiddenidinput')!='':
            print('-------')
            print(request.form.get('hiddenidinput'))
            id = int(request.form.get('hiddenidinput'))#this is update
            update_dict= dict(request.form)
            update_dict.pop('hiddenidinput')
            print(update_dict)
            for k in update_dict:
                update_dict[k] = update_dict[k][0]
            print(update_dict)
            MarketSupplyer.query.filter(MarketSupplyer.id==id).update(update_dict)
            try:
                db.session.commit()
                return jsonify({"success":True})
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify({"success":False})
        _m = MarketSupplyer(
            supplyer_id=request.form.get('supplyer_id'),
            name=request.form.get('name'),
            name_short=request.form.get('name_short'),
            address=request.form.get('address'),
            telephone=request.form.get('telephone'),
            email=request.form.get('email'),
            contact=request.form.get('contact'),
            contact_phone=request.form.get('contact_phone'),
            comment=request.form.get('comment'),
        )
        db.session.add(_m)
        print('==========')
        try:
            db.session.commit()
            return jsonify({"success":True})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"success":False})
    elif request.method=='DELETE':
        if not str(request.values.get('id')).isdigit():
            abort(400)
        id = int(request.values.get('id'))
        MarketSupplyer.query.filter(MarketSupplyer.id==id).update({'delete':True})
        try:
            db.session.commit()
            return jsonify({'success':True})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success':False})
    elif request.method=='PUT':
        pass
    else:
        abort(405)

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