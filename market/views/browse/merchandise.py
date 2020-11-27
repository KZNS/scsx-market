from flask import Blueprint, render_template, request, url_for, flash, redirect, abort, g, jsonify
from market.models import MarketMerchandise, db
from market.views.browse import browse
from market.utils import hash_password
from sqlalchemy import and_


@browse.route("/merchandiseinfo",methods=['GET'])
def merchandise_home():
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


@browse.route("/merchandise", methods=['GET'])
def merchandise():
    return render_template('browse_merchandise.html', title='商品查询')
