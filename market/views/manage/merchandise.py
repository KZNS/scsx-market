from flask import Blueprint, render_template, request, url_for, flash, redirect, abort, g, jsonify
from market.models import MarketMerchandise, db
from market.views.manage import manage
from market.utils import hash_password
from sqlalchemy import and_


@manage.route("/merchandiseinfo",methods=['GET','POST','DELETE'])
def merchandise_home():
    if request.method=='GET':
        #### START FUZZY SEARCH ####
        args_dict = dict(request.values)
        query_dict = {}
        for k in args_dict:
            if args_dict[k]!='' and hasattr(MarketMerchandise,k):
                query_dict[k]=args_dict[k]

        data = MarketMerchandise.query.filter(MarketMerchandise.delete!=True)
        for k in query_dict:
            data = data.filter(getattr(MarketMerchandise,k).like('%%'+query_dict[k]+'%%'))
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
            if 'merchandise_id' in update_dict.keys():
                update_dict.pop('merchandise_id')
            # for k in update_dict:
            #     update_dict[k] = update_dict[k][0]
            print(update_dict)
            MarketMerchandise.query.filter(MarketMerchandise.id==id).update(update_dict)
            try:
                db.session.commit()
                return jsonify({"success":True})
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify({"success":False})
        _m = MarketMerchandise(
            merchandise_id=request.form.get('merchandise_id'),
            name=request.form.get('name'),
            unit_price=request.form.get('unit_price'),
            supplyer_id=request.form.get('supplyer_id'),
            description=request.form.get('description'),
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
        MarketMerchandise.query.filter(MarketMerchandise.id==id).update({'delete':True})
        try:
            db.session.commit()
            return jsonify({'success':True})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success':False})


@manage.route('/merchandise/batchadd', methods=['POST'])
def merchandise_batchadd():
    batch = request.get_json().get('info')
    print(batch)
    merchandises = batch.split('\n')
    print(merchandises)
    
    for merchandise in merchandises:
        merchandise=merchandise.split(',')
        db.session.add(MarketMerchandise(
            merchandise_id=merchandise[0],
            name=merchandise[1],
            unit_price=merchandise[2],
            supplyer_id=merchandise[3],
            description=merchandise[4],
            comment=merchandise[5]
        ))
    try:
        db.session.commit()
        return jsonify({"success":True})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"success":False})


@manage.route("/merchandise", methods=['GET'])
def manage_merchandise():
    return render_template('manage_merchandise.html', title='商品管理')
