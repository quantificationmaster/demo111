from exts import db
from flask import Blueprint, render_template, request
from models import Teacher, Course, Student
from flask import session, redirect

r1 = Blueprint("rrr", __name__, url_prefix='/')

def cun(id):
    k =Teacher.query.filter_by(teachername=id).first()
    if k!=None:
        return 0
    else:
        return 1
@r1.route('/reg',methods=['POST','GET'])
def reg():
    if request.method == 'GET':
        return render_template('reg.html')
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    if cun(user)==1:
        k1=Teacher(teachername=user,pwd=pwd)
        db.session.add(k1)
        db.session.commit()
        return redirect('/login')
    else:
        error='账号已注册'
        return render_template('reg.html', error=error)

