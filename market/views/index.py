from flask import Blueprint,render_template,url_for,session,redirect
index = Blueprint("index",__name__,template_folder='templates',static_folder='static')

@index.route("/")
def helo():
    return render_template('index.html',login_url = url_for('user.log'),register_url = url_for('user.reg'))

@index.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.helo'))