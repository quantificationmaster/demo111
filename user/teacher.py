import xlrd
from flask import Blueprint, render_template, session, request, redirect,g
from exts import db
from models import Teacher,Course,Student,Late
from flask import url_for
from datetime import datetime
import os

tea = Blueprint("teacher", __name__, url_prefix='/')





@tea.route('/addclass',methods=['POST'])
def addclass():
    if request.method=='POST':
        file=request.files['file']
        f = file.read()
        # path=os.path.join('/upload',file.filename)
        # file.save(path)
        clinic_file = xlrd.open_workbook(file_contents=f)
        table = clinic_file.sheet_by_index(0)
        nrows = table.nrows
        for i in range(1, nrows):
            row_date = table.row_values(i)
            print(row_date)
            teachername = row_date[1]
            coursename = row_date[0]
            studentname = row_date[2]
            studentid = row_date[4]
            stugender =row_date[3]
            latecount = row_date[5]
            tche = Teacher.query.filter_by(teachername=teachername)
            if tche == None:
                tea = Teacher(teachername=teachername)
                db.session.add(tea)
                db.session.commit()
            tc = Teacher.query.filter_by(teachername=teachername).first()
            if tc == None:
                cou = Course(cid=coursename, tid=tc.id)
                db.session.add(cou)
                db.session.commit()
            cs = Course.query.filter_by(cid=coursename).first()
            sc=Student.query.filter_by(studentname=studentname).first()
            if not sc:
                stu = Student(studentname=studentname, student_gender=stugender, student_id=studentid, scid=cs.id,
                              latecount=latecount)
                db.session.add(stu)
            else:
                sc.student_id=studentid
                sc.student_gender=stugender
                sc.scid=cs.id
                sc.latecount=latecount
                db.session.add(sc)
        db.session.commit()
        return redirect('/login')

@tea.route('/teacher/<user>')
def index(user):
    results = Teacher.query.filter_by(teachername=user).first()
    print(results.course[0].cid)
    return render_template('teacher.html', result=results)


@tea.route('/teacher/course/<cname>')
def querycname(cname):
    result = Course.query.filter_by(cid=cname).first()
    print(result.sc[0].studentname)
    return render_template('course.html', courses=result)

@tea.route('/courseedit', methods=['GET', 'POST'])
def edit():
    cour = request.args.get('cour')
    id = request.args.get('id')
    late=request.args.get('late')
    if request.method == "GET":
        return render_template('course_edit.html',coursename=cour,id=id,late=late)
    course=request.form.get('coursename')
    studentname=request.form.get('studentname')
    latecount = request.form.get('latecount')
    cou =Course.query.filter_by(cid=course).first()
    icou=cou.id
    stu1=Student.query.filter_by(scid=icou).filter_by(studentname=studentname).first()
    stu1.latecount=latecount
    db.session.add(stu1)
    db.session.commit()
    return redirect('/login')

@tea.route('/delete')
def delete():
    cour = request.args.get('cour')
    id = request.args.get('id')
    late = request.args.get('late')
    cou =Course.query.filter_by(cid=cour).first()
    stu =Student.query.filter_by(scid=cou.id).filter_by(studentname=id).first()
    db.session.delete(stu)
    db.session.commit()
    return redirect(request.referrer)

@tea.route('/late/<name>/<course>',methods=['POST','GET'])
def late(name,course):
    k=Late.query.filter_by(coursename=course).filter_by(studentname=name).all()
    # now =datetime.now()
    # date=now.strftime("%Y-%m-%d")
    # ll =Late(coursename=1,studentname=2,lateday=date)
    # db.session.add(ll)
    # db.session.commit()
    return render_template('late.html',result=k)
