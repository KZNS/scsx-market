from flask import Blueprint, render_template, request, url_for, flash, redirect, abort, g, jsonify
from market.models import MarketStaff, db
from market.views.manage import manage
from market.utils import hash_password
from sqlalchemy import and_


@manage.route("/staff", methods=['GET'])
def manage_staff():
    return render_template('manage_staff.html', title='员工管理')

@manage.route('/staff/batchadd', methods=['POST'])
def staff_batchadd():
    batch = request.get_json().get('info')
    print(batch)
    staffs = batch.split('\n')
    print(staffs)

    for staff in staffs:
        staff=staff.split(',')
        db.session.add(MarketStaff(
            staff_id=staff[0],
            name=staff[1],
            password_hash=hash_password('d1f43251239d2ed9c45555ff82c315e2'),
            level=staff[2],
            telephone=staff[3],
            salary=staff[4],
            comment=staff[5],
        ))
    try:
        db.session.commit()
        return jsonify({"success":True})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"success":False})


@manage.route("/staffinfo", methods=['GET', 'POST', 'DELETE'])
def staff_home():
    if request.method == 'GET':
        staff_id = request.values.get('staff_id')
        name = request.values.get('name')
        level = request.values.get('level')
        telephone = request.values.get('telephone')
        salary = request.values.get('salary')
        comment = request.values.get('comment')

        data = MarketStaff.query.filter(MarketStaff.delete == False)

        if (staff_id):
            data = data.filter(MarketStaff.staff_id.like('%%' + staff_id + '%%'))
        if (name):
            data = data.filter(MarketStaff.name.like('%%' + name + '%%'))
        if (level):
            data = data.filter(MarketStaff.level.like('%%' + level + '%%'))
        if (telephone):
            data = data.filter(MarketStaff.telephone.like('%%' + telephone + '%%'))
        if (salary):
            data = data.filter(MarketStaff.salary.like('%%' + salary + '%%'))
        if (comment):
            data = data.filter(MarketStaff.comment.like('%%' + comment + '%%'))

        data = data.all()
        result = []
        for s in data:
            result.append(s.todict())
        return jsonify(result)

    elif request.method == 'POST':
        if request.form.get('hiddenidinput')!='':
            print('-------')
            print(request.form.get('hiddenidinput'))
            id = int(request.form.get('hiddenidinput'))#this is update
            update_dict= dict(request.form)
            update_dict.pop('hiddenidinput')
            print(update_dict)
            if id == g.id and update_dict['level'] != 'admin':
                return jsonify({"success":False, 'self':True})
            if 'password' in update_dict.keys():
                if update_dict['password'] and update_dict['password'] != '':
                    update_dict['password_hash'] = hash_password(update_dict['password'])
                update_dict.pop('password')
            if 'staff_id' in update_dict.keys():
                update_dict.pop('staff_id')
            # for k in update_dict:
            #     update_dict[k] = update_dict[k][0]
            print(update_dict)
            MarketStaff.query.filter(and_(MarketStaff.id == id, MarketStaff.delete == False)).update(update_dict)
            try:
                db.session.commit()
                return jsonify({"success":True, 'self':False})
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify({"success":False, 'self':False})
        item = MarketStaff(
            staff_id=request.form.get('staff_id'),
            name=request.form.get('name'),
            password_hash=hash_password(request.form.get('password')),
            level=request.form.get('level'),
            telephone=request.form.get('telephone'),
            salary=request.form.get('salary'),
            comment=request.form.get('comment')
        )
        print(item)
        db.session.add(item)
        try:
            db.session.commit()
            return jsonify({"success":True})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"success":False})

    elif request.method == 'DELETE':
        if not str(request.values.get('id')).isdigit():
            abort(400)
        id = int(request.values.get('id'))
        if id == g.id:
            return jsonify({'success':False, 'self':True})
        MarketStaff.query.filter(MarketStaff.id == id).update({'delete': True})
        try:
            db.session.commit()
            return jsonify({'success':True, 'self':False})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'success':False, 'self':False})
