from flask import Blueprint, render_template, request, url_for, flash, redirect, abort
from market.models import MarketStaff, db
from market.views.manage import manage
from market.utils import hash_password
from sqlalchemy import and_


@manage.route("/staff", methods=['GET'])
def staff_query():
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

    return render_template('manage_staff.html', data=data, title='Staff Management')


@manage.route("/staff/add", methods=['GET', 'POST'])
def staff_add():
    if request.method == 'GET':
        return render_template('manage_staff_add.html', title='Add Staff')
    elif request.method == 'POST':
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
            flash('增加成功')
        except Exception as e:
            print(e)
            db.session.rollback()
            flash('增加失败')
        return redirect(url_for('manage.staff_query', timeout=True))


@manage.route("/staff/del/<int:id>", methods=['DELETE'])
def staff_delete(id):
    MarketStaff.query.filter(MarketStaff.id == id).update({'delete': True})
    try:
        db.session.commit()
        return 'succeed'
    except Exception as e:
        print(e)
        db.session.rollback()
        return 'fail'

@manage.route("/staff/modify/<int:id>", methods=['GET', 'POST'])
def staff_modify(id):
    if request.method == 'GET':
        item = MarketStaff.query.filter(and_(MarketStaff.id == id, MarketStaff.delete == False))[:]
        print(item)
        if not item:
            abort(404)
        print('hello')
        return render_template('manage_staff_modify.html', item=item[0], title='Modify Staff')
    elif request.method == 'POST':
        d = {
            'name' : request.form.get('name'),
            'level' : request.form.get('level'),
            'telephone' : request.form.get('telephone'),
            'salary' : request.form.get('salary'),
            'comment' : request.form.get('comment')
        }
        password = request.form.get('password')
        if password and password != '':
            d['password_hash'] = hash_password(password)
        print(request.values.__dict__)
        MarketStaff.query.filter(MarketStaff.id == id).update(d)
        try:
            db.session.commit()
            flash('修改成功')
        except Exception as e:
            print(e)
            db.session.rollback()
            flash('修改失败')
        return redirect(url_for('manage.staff_query', timeout=True))
