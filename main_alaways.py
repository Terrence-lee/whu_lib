from main import main,get_proxy
import time
import datetime
import utils
import pymysql
import threading
#要进行的工作是：（先对数据库的时间进行排序order？）读取时间，和本地时间对比（满足一定条件），进行相对应的赋值
print(datetime.datetime.now().date())
#找出所有预约日期为第二天的数据
def get_data():
    nextday=(datetime.datetime.now()+datetime.timedelta(days=1)).date().strftime("%Y-%m-%d") #第二天
    sql_info="select * from seat where day='%s' or day='everyday'"%(nextday)
    con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
    cur = con.cursor()
    cur.execute(sql_info)
    data = cur.fetchall()
    print(type(data))
    print(data)
    return data
#输入时间，返回分钟数。输入的时间是08：00这种格式，冒号前面要有两位
def time_to_minute(i):
    if i[0]=='0':
        return int(eval(i[1]))*60+int(eval(i[3:]))
    else:
        return int(eval(i[:2])) * 60 + int(eval(i[3:]))

proxy=get_proxy()


def order(account,password,begintime,endtime,*seatid):
    print(1)
    try:
        localtime=time.localtime()
        print(localtime)
        #设置等待时间时间
        reserver_time=utils.get_reserve_date()[0]+" 22:43"
        #reserver_time="2021-05-09 22:43"
        print("reserver_time: ",reserver_time)
        reserver_time = datetime.datetime.strptime(reserver_time, "%Y-%m-%d %H:%M")
        now_time=datetime.datetime.now()
        sleep_time=(reserver_time-now_time).seconds
        print("sleep_time: ",sleep_time)
        time.sleep(sleep_time)
        while localtime[3]==22 and localtime[4]==43:
            time.sleep(50)
            localtime = time.localtime()
            print("sleeping1……")
            if localtime[3]==22 and localtime[4]==44: #在这里先获取token？
                #阿里云服务器必须先获取代理IP，获取失败则无法继续
                while 1:
                    print("获取ip：",end="")
                    try:
                        proxy=get_proxy()
                        if proxy:
                            print(proxy)
                            break
                    except:
                        continue
                m=0
                while True:
                    time.sleep(0.5)
                    print("sleeping2……")
                    localtime = time.localtime()
                    if localtime[3]==22 and localtime[4]==45 and m<=6:
                        print("开始第一次预约尝试")
                        success_order=main(account,password,seatid[0],begintime,endtime,proxy)
                        print("第一次尝试的结果",success_order)
                        if success_order:
                            return 1
                        elif len(seatid)==2:#更换第二个座位选项
                            print("开始第二次预约尝试")
                            success_order=main(account,password,seatid[1],begintime,endtime,proxy)
                            if success_order:
                                print("第二次尝试的结果", success_order)
                                return 1
                            elif len(seatid)>2:#更换第二个座位选项
                                print("开始第三次预约尝试")
                                success_order=main(account,password,seatid[2],begintime,endtime,proxy)
                                if success_order:
                                    print("第二次尝试的结果", success_order)
                                    return 1
                        m+=1
                    if not success_order and m>5:
                        return 0
    except:
        return 0


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self,account, password, begintime, endtime,*seatid,):
        threading.Thread.__init__(self)
        self.account = account
        self.password=password
        self.begintime=begintime
        self.endtime=endtime
        self.seatid=seatid


    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        order(self.account,self.password,self.begintime,self.endtime,self.seatid)

m=0
thread_order=[]
while 1:
    try:
        #每天22：42分之前都可以提交预约
        reserver_time = utils.get_reserve_date()[0] + " 22:42"
        # reserver_time="2021-05-09 22:43"
        print("reserver_time: ", reserver_time)
        reserver_time = datetime.datetime.strptime(reserver_time, "%Y-%m-%d %H:%M")
        now_time = datetime.datetime.now()
        sleep_time = (reserver_time - now_time).seconds
        print("sleep_time: ", sleep_time)
        time.sleep(sleep_time)
        data=get_data()
        con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
        cur = con.cursor()
        for i in data:
            m+=1
            uid = i[1]
            begintime = time_to_minute(i[4])
            endtime = time_to_minute(i[5])
            seatid = i[2]
            if len(i) == 9:
                seatid2 = i[8]
            if len(i) == 10:
                seatid3 = i[9]
            sql_get_userinfo = "select * from user where account='%s'" % uid
            cur = con.cursor()
            cur.execute(sql_get_userinfo)
            data_user = cur.fetchall()
            account = data_user[0][0]
            password = data_user[0][1]
            print("data_user:", data_user)
            print(account, password)
            if len(i) == 8:
                thread = myThread(account, password, begintime, endtime, seatid)
                thread_order.append(thread)
            if len(i) == 9:
                thread = myThread(account, password, begintime, endtime, seatid2)
                thread_order.append(thread)
            if len(i) == 10:
                thread = myThread(account, password, begintime, endtime, seatid2,seatid3)
                thread_order.append(thread)
        cur.close()
        con.close()
        for thread in thread_order:
            thread.start()
        thread_order=[]
        #time.sleep(86400) #每24小时执行一波
    except:
        continue

    # order("2018301040124", "17071X", 480, 1350,9390)