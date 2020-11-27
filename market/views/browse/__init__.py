from flask import Blueprint
from market.interceptors import login_required
browse = Blueprint("browse",__name__,template_folder='templates',static_folder='static',url_prefix='/browse')
from market.views.browse import home,order
@browse.before_request
@login_required
def before_bp():
    pass