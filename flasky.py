from flask import Flask, render_template, request, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from werkzeug.utils import redirect
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
import sqlite3
# con = sqlite3.connect(r"E:\program\whulib\data.sqlite")#****这部分上传到服务器的时候要进行替换
# cur = con.cursor()

#获取路径 此处先获取该文档路径，然后转化为绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))
#初始化
app = Flask(__name__)
#将路径保存到环境变量config中
app.config['SQLALCHEMY_DATABASE_URI'] =\
         'sqlite:///' + os.path.join(basedir, 'data.sqlite')
#下面这句是为了在不需要跟踪对象变化时降低内存消耗的配置
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#初始化数据库，从此db对象就是SQLAlchemy类的实例，可以被调用各种功能
db = SQLAlchemy(app)

app.config['SECRET_KEY']='test7878'


bootstarp = Bootstrap(app)
#moment = Moment(app)

#数据库
class Account(db.Model):
    __tablename__='accounts'
    id = db.Column(db.Integer,primary_key=True)
    acc=db.Column(db.String(64),unique=True)
    password=db.Column(db.String(64))
    users=db.relationship('User',backref="account")

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    site=db.Column(db.String(64))
    seat=db.Column(db.String(64))
    seatId=db.Column(db.String(64))
    day = db.Column(db.String(64))
    begintime = db.Column(db.String(64))
    endtime = db.Column(db.String(64))
db.drop_all()
db.create_all()

@app.route('/',methods=['POST','GET'])
def hello_world():
    return render_template('hello.html',user=db.session.query(User).all())

@app.route('/result',methods=['POST','GET'])
def result():
    print(str(request.form["seat"])[4:])
    user=User(site= str(request.form["site"])+" "+str(request.form["seat0"]),day=str(request.form["day"]),seatId=str(request.form["seat"])[4:],seat=str(request.form["seat"])[:3],begintime=str(request.form["begintime"]),endtime=str(request.form["endtime"]))
    #cancel=request.form["cancel"]
    db.session.add(user)
    db.session.commit()
    print("数据库查询：")
    print(db.session.query(User).all())
    return render_template('result.html',user=db.session.query(User).all())

@app.route('/cancel',methods=['POST','GET'])
def cancel():
    #进行删除操作，从数据库中删除该条内容，通过where来查找吧
    #如何删除行？？？
    print((int(request.form["id"])))
    a = User.query.get(int(request.form["id"]))
    db.session.delete(a)
    db.session.commit()
    return render_template('result.html',user=db.session.query(User).all())

@app.route('/database',methods=['POST','GET'])
def database():
    #此处应该对post请求进行验证
    pass



app.run()