from market.views.manage import manage
from flask import render_template,g,jsonify
from market.models import db,MarketSupplyer


@manage.route("/supplyerinfo",methods=['GET','POST'])
def supplyer_home():
    suppliers = MarketSupplyer.query.all()
    result = []
    for s in suppliers:
        result.append(s.todict())
    return jsonify(result)