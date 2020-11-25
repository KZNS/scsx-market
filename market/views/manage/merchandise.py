from flask import Blueprint, render_template, request, url_for, flash, redirect, abort
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
