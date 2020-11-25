from flask import Blueprint, render_template, request, url_for, flash, redirect, abort, g
from market.models import MarketMerchandise, db
from market.views.manage import manage
from market.utils import hash_password
from sqlalchemy import and_


@manage.route("/merchandise", methods=['GET'])
def merchandise():
    merchandise_id = request.values.get('merchandise_id')
    name = request.values.get('name')
    unit_price = request.values.get('unit_price')
    supplyer_id = request.values.get('supplyer_id')
    description = request.values.get('description')
    comment = request.values.get('comment')

    data = MarketMerchandise.query.filter(MarketMerchandise.delete == False)

    if (merchandise_id):
        data = data.filter(MarketMerchandise.merchandise_id.like('%%' + merchandise_id + '%%'))
    if (name):
        data = data.filter(MarketMerchandise.name.like('%%' + name + '%%'))
    if (unit_price):
        data = data.filter(MarketMerchandise.unit_price.like('%%' + unit_price + '%%'))
    if (supplyer_id):
        data = data.filter(MarketMerchandise.supplyer_id.like('%%' + supplyer_id + '%%'))
    if (description):
        data = data.filter(MarketMerchandise.description.like('%%' + description + '%%'))
    if (comment):
        data = data.filter(MarketMerchandise.comment.like('%%' + comment + '%%'))

    return render_template('manage_merchandise.html', data=data, title='Merchandise Management')

@manage.route("/merchandise/add", methods=['GET', 'POST'])
def merchandise_add():
    if request.method == 'GET':
        return render_template('manage_merchandise_add.html', title='Add Merchandise')
    elif request.method == 'POST':
        item = MarketMerchandise(
            merchandise_id=request.form.get('merchandise_id'),
            name=request.form.get('name'),
            unit_price=request.form.get('unit_price'),
            supplyer_id=request.form.get('supplyer_id'),
            description=request.form.get('description'),
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
        return redirect(url_for('manage.merchandise', timeout=True))


@manage.route("/merchandise/del/<int:id>", methods=['DELETE'])
def merchandise_delete(id):
    if id == g.id:
        return 'self'
    MarketMerchandise.query.filter(MarketMerchandise.id == id).update({'delete': True})
    try:
        db.session.commit()
        return 'succeed'
    except Exception as e:
        print(e)
        db.session.rollback()
        return 'fail'

@manage.route("/merchandise/modify/<int:id>", methods=['GET', 'POST'])
def merchandise_modify(id):
    if request.method == 'GET':
        item = MarketMerchandise.query.filter(and_(MarketMerchandise.id == id, MarketMerchandise.delete == False))[:]
        print(item)
        if not item:
            abort(404)
        return render_template('manage_merchandise_modify.html', item=item[0], title='Modify Merchandise')
    elif request.method == 'POST':
        d = {
            'name' : request.form.get('name'),
            'unit_price' : request.form.get('unit_price'),
            'supplyer_id' : request.form.get('supplyer_id'),
            'description' : request.form.get('description'),
            'comment' : request.form.get('comment')
        }
        print(request.values.__dict__)
        MarketMerchandise.query.filter(MarketMerchandise.id == id).update(d)
        try:
            db.session.commit()
            flash('修改成功')
        except Exception as e:
            print(e)
            db.session.rollback()
            flash('修改失败')
        return redirect(url_for('manage.merchandise', timeout=True))

