from flask import Flask,render_template, redirect, request, url_for, flash,session
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_login import login_user, logout_user, login_required, \
    current_user
from werkzeug.utils import redirect
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from proxy_matain import get_proxy
from main import AppRes


#获取路径 此处先获取该文档路径，然后转化为绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))
#初始化
app = Flask(__name__)
#将路径保存到环境变量config中

app.secret_key = 'CSaSvOU6x1iMb15s+Gsq5TuKYSbREcBZ/g1Gjh9nsec='
app.config['PERMANENT_SESSION_LIFETIME'] = 600


bootstarp = Bootstrap(app)
#moment = Moment(app)

#数据库
# class Account(db.Model):
#     __tablename__='accounts'
#     id = db.Column(db.Integer,primary_key=True)
#     acc=db.Column(db.String(64),unique=True)
#     password=db.Column(db.String(64))
#     users=db.relationship('User',backref="account")

# class User(db.Model):
#     __tablename__='users'
#     id = db.Column(db.Integer,primary_key=True)
#     site=db.Column(db.String(64))
#     seat=db.Column(db.String(64))
#     seatId=db.Column(db.String(64))
#     day = db.Column(db.String(64))
#     begintime = db.Column(db.String(64))
#     endtime = db.Column(db.String(64))
# db.drop_all()
# db.create_all()


class LoginForm(FlaskForm):
    account = StringField('学号', validators=[DataRequired(), Length(1, 64),])
    password = PasswordField('图书馆密码', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')





@app.route('/',methods=['POST','GET'])
def index():
    return render_template('first.html')

@app.route('/user',methods=['POST','GET'])
def user():
    if 'username' in session and session['username']:
        con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu",charset='utf8')
        cur = con.cursor()
        uid=session['username']
        sql_search = "select * from seat where uid=%s"%uid
        cur.execute(sql_search)
        data = cur.fetchall()
        cur.close()
        con.close()
        return render_template('hello.html',user=data) #通过修改user需要的data就实现了显示不同数据；此处显示登录用户的数据
    return redirect(url_for('login'))

@app.route('/result',methods=['POST','GET'])
def result():
    if 'username' in session and session['username']:
        #连接数据库
        con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
        cur = con.cursor()
        #user=User(
        #获取表单
        uid=eval(session["username"]) #这部分之后会替换掉，自动获取登录的用户的uid
        libsite= str(request.form["site"])+" "+str(request.form["seat0"])
        day=str(request.form["day"])
        everyday=str(request.form["everyday"])
        if everyday=="1":
            day="everyday"

        seatId=str(request.form["seat"]).split('_')[1]
        seatname=str(request.form["seat"]).split('_')[0]
        begintime=str(request.form["begintime"])
        endtime=str(request.form["endtime"])
        allday = str(request.form["allday"])
        if allday == "1":
            begintime = "08:00"
            endtime = "22:30"
        print(uid,seatId,day,begintime,endtime,libsite,seatname)
        #插入数据库
        sql_user = "INSERT INTO user(account,password,authid) VALUES ('2018301040124','17071X','e-stu');"
        sql_seat="INSERT INTO seat(uid,seatid,day,begintime,endtime,libsite,seatname) VALUES (%d,'%s','%s','%s','%s','%s',%s);"%(uid,seatId,day,begintime,endtime,libsite,seatname)
        cur.execute(sql_seat)
        con.commit()
        sql_search = "select * from seat where uid=%s"%uid
        cur.execute(sql_search)
        data = cur.fetchall()
        #cancel=request.form["cancel"]
        # db.session.add(user)
        # db.session.commit()

        #print(db.session.query(User).all())
        cur.close()
        con.close()
        print("数据库查询：", data)
        return render_template('result.html',user=data)
    return redirect(url_for('login'))

@app.route('/cancel',methods=['POST','GET'])
def cancel():
    #进行删除操作，从数据库中删除该条内容，通过where来查找吧
    #如何删除行？？？
    if 'username' in session and session['username']:
        con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
        cur = con.cursor()
        uid=eval(session["username"])
        print("test")
        id=eval(request.form["cancel_id"])  #如何获得座位的id？
        print("id:",id)
        sql_cancel = "DELETE FROM seat WHERE id=%d"%id
        cur.execute(sql_cancel)
        con.commit()
        sql_search = "select * from seat where uid=%s" % uid
        cur.execute(sql_search)
        data = cur.fetchall()
        return render_template('result.html',user=data)
    return redirect(url_for('login'))

#管理员界面中显示用户信息的
@app.route('/user_info',methods=['POST','GET'])
def user_info():
    #进行删除操作，从数据库中删除该条内容，通过where来查找吧
    #如何删除行？？？
    try:
        sql_admin_info="select count(*) from admin where account='%s'"%session['username']
        con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
        cur = con.cursor()
        cur.execute(sql_admin_info)
        admin = cur.fetchall()
        admin = admin[0][0]
    except:
        return redirect(url_for('login'))
    if ('username' in session) and admin:
        #显示用户页面
        #这里使用了表连接：除了user的信息，还希望能够获得到user有几条预约记录
        sql_user_info='''
        select account,password,authid from user   

        '''
        cur.execute(sql_user_info)
        data = cur.fetchall()
        #cancel=request.form["cancel"]
        # db.session.add(user)
        # db.session.commit()
        #print(db.session.query(User).all())
        cur.close()
        con.close()
        print("数据库查询：", data)
        return render_template('admin_user_info.html',user=data)
    return redirect(url_for('login'))

#管理员界面中显示座位信息的
@app.route('/seat_info',methods=['POST','GET'])
def seat_info():
    #进行删除操作，从数据库中删除该条内容，通过where来查找吧
    #如何删除行？？？
    sql_admin_info="select count(*) from admin where account='%s'"%session['username']
    con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
    cur = con.cursor()
    cur.execute(sql_admin_info)
    admin = cur.fetchall()
    admin = admin[0][0]
    if ('username' in session) and admin:
        #显示用户页面
        sql_user_info="select * from seat"
        cur.execute(sql_user_info)
        data = cur.fetchall()
        cur.close()
        con.close()
        print("数据库查询：", data)
        return render_template('admin_seat_info.html',user=data)
    return redirect(url_for('login'))

#按照特定的用户名进行检索
@app.route('/seat_info_uid',methods=['POST','GET'])
def seat_info_uid():
    #进行删除操作，从数据库中删除该条内容，通过where来查找吧
    #如何删除行？？？
    sql_admin_info="select count(*) from admin where account='%s'"%session['username']
    con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
    cur = con.cursor()
    cur.execute(sql_admin_info)
    admin = cur.fetchall()
    admin = admin[0][0]
    uid=request.form["uid"]
    print(uid)
    if ('username' in session) and admin:
        #显示用户页面
        sql_user_info="select * from seat where uid LIKE '%%%s%%'"%uid
        cur.execute(sql_user_info)
        data = cur.fetchall()
        cur.close()
        con.close()
        print("数据库查询：", data)
        return render_template('admin_seat_info.html',user=data)
    return redirect(url_for('login'))


#按照特定的日期进行检索
@app.route('/seat_info_date',methods=['POST','GET'])
def seat_info_date():
    #进行删除操作，从数据库中删除该条内容，通过where来查找吧
    #如何删除行？？？
    sql_admin_info="select count(*) from admin where account='%s'"%session['username']
    con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
    cur = con.cursor()
    cur.execute(sql_admin_info)
    admin = cur.fetchall()
    admin = admin[0][0]
    date=request.form["date"]
    if ('username' in session) and admin:
        #显示用户页面
        sql_user_info="select * from seat where day LIKE '%%%s%%'"%date
        cur.execute(sql_user_info)
        data = cur.fetchall()
        cur.close()
        con.close()
        print("数据库查询：", data)
        return render_template('admin_seat_info.html',user=data)
    return redirect(url_for('login'))

#按照特定的座位号进行检索
@app.route('/seat_info_seatid',methods=['POST','GET'])
def seat_info_seatid():
    #进行删除操作，从数据库中删除该条内容，通过where来查找吧
    #如何删除行？？？
    sql_admin_info="select count(*) from admin where account='%s'"%session['username']
    con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
    cur = con.cursor()
    cur.execute(sql_admin_info)
    admin = cur.fetchall()
    admin = admin[0][0]
    seatid=request.form["seatid"]
    if ('username' in session) and admin:
        #显示用户页面
        sql_user_info="select * from seat where seatid LIKE '%%%s%%'"%seatid
        cur.execute(sql_user_info)
        data = cur.fetchall()
        cur.close()
        con.close()
        print("数据库查询：", data)
        return render_template('admin_seat_info.html',user=data)
    return redirect(url_for('login'))

#按照特定的场馆名进行检索
@app.route('/seat_info_seatname',methods=['POST','GET'])
def seat_info_seatname():
    #进行删除操作，从数据库中删除该条内容，通过where来查找吧
    #如何删除行？？？
    sql_admin_info="select count(*) from admin where account='%s'"%session['username']
    con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
    cur = con.cursor()
    cur.execute(sql_admin_info)
    admin = cur.fetchall()
    admin = admin[0][0]
    seatname=request.form["seatname"]
    if ('username' in session) and admin:
        #显示用户页面
        sql_user_info="select * from seat where seatname LIKE '%%%s%%'"%seatname
        cur.execute(sql_user_info)
        data = cur.fetchall()
        cur.close()
        con.close()
        print("数据库查询：", data)
        return render_template('admin_seat_info.html',user=data)
    return redirect(url_for('login'))


#管理员界面中，删除用户信息的；添加修改用户信息？如修改用户的授权码？或者预约时间
@app.route('/delete_user',methods=['POST','GET'])
def delete_user():
    #进行删除操作，从数据库中删除该条内容，通过where来查找吧
    #如何删除行？？？
    #对于管理员权限的认证：
    sql_admin_info="select count(*) from admin where account='%s'"%session['username']
    con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
    cur = con.cursor()
    cur.execute(sql_admin_info)
    admin=cur.fetchall()
    admin=admin[0][0]
    if ('username' in session) and admin:
        account=eval(request.form["account"])
        print("account",account)
        sql_delete_user = "DELETE FROM user WHERE account=%d"%account
        cur.execute(sql_delete_user)
        con.commit()
        sql_search = "select * from user"
        cur.execute(sql_search)
        data = cur.fetchall()
        cur.close()
        con.close()
        return render_template('admin_user_info.html',user=data)
    return redirect(url_for('login'))


#管理员界面中，删除用户信息的；添加修改用户信息？如修改用户的授权码？或者预约时间
@app.route('/delete_seat',methods=['POST','GET'])
def delete_seat():
    #进行删除操作，从数据库中删除该条内容，通过where来查找吧
    #如何删除行？？？
    #对于管理员权限的认证：
    sql_admin_info="select count(*) from admin where account='%s'"%session['username']
    con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
    cur = con.cursor()
    cur.execute(sql_admin_info)
    admin=cur.fetchall()
    admin=admin[0][0]
    if ('username' in session) and admin:
        id=eval(request.form["id"])
        sql_delete_user = "DELETE FROM seat WHERE id=%d"%id
        cur.execute(sql_delete_user)
        con.commit()
        sql_search = "select * from seat"
        cur.execute(sql_search)
        data = cur.fetchall()
        cur.close()
        con.close()
        return render_template('admin_seat_info.html',user=data)
    return redirect(url_for('login'))


@app.route('/database',methods=['POST','GET'])
def database():
    #此处应该对post请求进行验证
    pass



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
        cur = con.cursor()
        sql="select * from user where account='%s'"%form.account.data
        cur.execute(sql)
        data = cur.fetchall()
        sql = "select * from admin where account='%s'" % form.account.data
        cur.execute(sql)
        data_admin = cur.fetchall()
        if data or data_admin:
            if data:
                user = data[0]
            else:
                user=None
            if data_admin:
                admin=data_admin[0]
            else:
                admin=None
            # print(data)
            # print(form.password.data)
            # print(user[2]==form.password.data)
            # print(user is not None)

            if user is not None and user[1]==form.password.data and user[1]:
                session['username']=user[0]
                # print("进入if")
                # print(0)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('user')
                cur.close()
                con.close()
                return redirect(next)
            elif admin is not None and admin[2]==form.password.data and admin[2]:
                session['username']=admin[1]
                cur.close()
                con.close()
                return redirect(url_for('user_info'))
            else:
                flash('Invalid account or password.')
                return render_template('login.html', form=form)
        else:
            user_info = {'username': '%s' %form.account.data , 'password': '%s' %form.password.data}
            order=AppRes(user_info,get_proxy()).login()
            print(order)
            if order: #需要写入
                sql_user = "INSERT INTO user(account,password,authid) VALUES ('%s','%s','e-stu');"%(form.account.data,form.password.data)
                cur.execute(sql_user)
                con.commit()
                # next = request.args.get('next')
                # print(next)
                # if next is None or not next.startswith('/'):
                #     next = url_for('user')
                cur.close()
                con.close()
                session['username'] = form.account.data
                return redirect(url_for('user'))
            else:
                cur.close()
                con.close()
                flash('Invalid account or password.')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/auth_info')
def auth_info():
    return render_template('my_info.html')




app.run()