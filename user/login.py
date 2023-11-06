from exts import db
from flask import  Blueprint,render_template,request
from models import Teacher,Course,Student
login = Blueprint("login", __name__, url_prefix='/')
def yanzheng():
    return 0
@login.route('/log')
def log():
    return 'hellp'

