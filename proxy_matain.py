import requests
import json
import pymysql
import utils
import datetime
import time
#从互联网获取代理节点
def pull_proxy():
    header={
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "User-Agent": "doSingle/11 CFNetwork/976 Darwin/18.2.0",
        "Accept-Language": "zh-cn",
        "Accept-Encoding": "gzip, deflate",
    }
    m = requests.get("http://user.xingsudaili.com:25434/jeecg-boot/extractIp/s?uid=1394303899117629442&orderNumber=CN2021051815141621&number=1&wt=json&randomFlag=false&detailFlag=true&useTime=30&region=",headers=header)
    print(m)
    b = json.loads(m.text)
    print(b)
    if b['success'] == True:
        n = b['result'][0]  # 124.230.8.126:36490,124.230.8.126,中国-湖南省-邵阳市-电信,1621733005,1621743805
        n = n.split(",")
        return "http://"+n[0]  # '124.230.8.126:36490'

#插入到数据库
def insert_sql():
    proxy = pull_proxy()
    print(proxy)
    sql_insert="INSERT INTO proxy values(null,'%s')"%proxy
    con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
    cur = con.cursor()
    cur.execute(sql_insert)
    con.commit()
#清空数据库
def delete_sql():
    sql_delete="TRUNCATE from proxy"
    con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
    cur = con.cursor()
    cur.execute(sql_delete)
    con.commit()
    return 1
#每天定时执行
def main():
    # reserver_time = utils.get_reserve_date()[0] + " 22:42"
    # # reserver_time="2021-05-09 22:43"
    # print("reserver_time: ", reserver_time)
    # reserver_time = datetime.datetime.strptime(reserver_time, "%Y-%m-%d %H:%M")
    # now_time = datetime.datetime.now()
    # sleep_time = (reserver_time - now_time).seconds
    # print("sleep_time: ", sleep_time)
    # time.sleep(sleep_time)
    delete_sql()
    insert_sql()



#用来获取proxy节点的函数，方便程序管理
def get_proxy():
    sql_delete = "select * from proxy"
    con = pymysql.connect(host="localhost", user="root", password="119cxy119", db="whu")
    cur = con.cursor()
    cur.execute(sql_delete)
    sql=cur.fetchall()
    sql=sql[-1]
    print(sql)
    return sql[1]

#此处就显示除了这个函数的重要性：
if __name__=='__main__':
    insert_sql()
    while 1:
        try:
            #get_proxy()
            main()
            time.sleep(60)
        except:
            continue

