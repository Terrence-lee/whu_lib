
#############################################################
#                        作者：我.doc
# Github地址：https://github.com/idocx/WHULibSeatReservation
#############################################################
import time
import datetime
from requests import Session
import json
import utils
import sqlite3


class AppRes(Session):
    #请求头
    default_header = {
        "Host": "seat.lib.whu.edu.cn:8443",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "User-Agent": "doSingle/11 CFNetwork/976 Darwin/18.2.0",
        "Accept-Language": "zh-cn",
        "Accept-Encoding": "gzip, deflate",
    }
    orgin_host = "https://seat.lib.whu.edu.cn:8443/"

    #有环境变量需要传入？
    def __init__(self, config):
        super(AppRes, self).__init__()
        self.headers.update(self.default_header)
        self.config = config
        #这里面？utils难道是自己定义的？
        self.reserve_date, self.is_tomorrow = utils.get_reserve_date()  # reserve_date是一个字符串类型
        self.login()

    #这是一个处理json的，用来提交请求，并返回json格式的数据
    def req_with_json(self, url, data=None):
        """
        用于处理返回值为json的请求
        :param data: POST请求中发送的内容
        :param url: string
        :return: dict
        """
        url = self.orgin_host + url
        if data:
            req = self.post(url, data=data)  #使用的是Session方法？
        else:
            req = self.get(url)
        response = req.text
        if response == "WHU Library seat reserving system is over loading," \
                       " please don't use un-offical applications!":
            raise Exception(
                """WHU Library seat reserving system is over loading, please don't use un-offical applications!
                武汉大学图书馆预约系统已经不堪重负，请不要使用非官方的预约应用！"""
            )
        return json.loads(response)

    #获取登录的token
    def login(self):
        """
            用于模拟自习助手的登陆，从而实现绕过验证码
            :return: token, string 系统用token验证身份
        """
        url = "rest/auth?username={0}&password={1}".format(self.config["username"], self.config["password"])
        response = self.req_with_json(url)
        if response["status"] == "fail":
            raise utils.LoginError("账号或密码不正确，请修改同目录下config.json中的账号和密码")
        token = response["data"]["token"]
        self.headers["token"] = token  # 自动更新headers，加入token记录登陆信息
        print("【APP端登陆成功】")

    #查询自己的座位信息
    def get_resevation_info(self):
        """
        查询当前的预约状态
        :return: 如果没有预约，则返回None；如果有，则返回一个seat_id的string，用于取消座位
        """
        url = "rest/v2/user/reservations"
        response = self.req_with_json(url)
        data = response["data"]
        if not data:
            print("当前没有预约")
            return (None,) * 3
        res_data = data[0]
        res_id = res_data["id"]
        seat_status = res_data["status"]
        seat_id = res_data["seatId"]
        seat_location = res_data["location"]
        start = res_data["begin"]
        end = res_data["end"]
        print("当前有一个位置在{}，时间为{}~{}的预约".format(seat_location, start, end))
        return seat_id, res_id, seat_status

    #预约座位
    def reserve_seat(self, seat_id, start_time, end_time):
        """
        预约座位
        :param seat_id: 所要预约的座位号
        :param start_time: 开始时间，特殊值为“now”
        :param end_time: 结束时间
        :return: 预约的请求号
        """
        url = "rest/v2/freeBook"
        # if not utils.is_reasonable_time(start_time, end_time, self.is_tomorrow):
        #     raise utils.TimeSetError("时间设置不正确，请重新设置")
        data_to_send = {
            "t": 1,
            "startTime": start_time,
            "endTime": end_time,
            "seat": seat_id,
            "date": self.reserve_date,
            "t2": 2
        } #这里的date是指年月日
        print("data_to_send: ",data_to_send)
        response = self.req_with_json(url=url, data=data_to_send)
        data = response["data"]
        if response["status"] == "success":
            location = data["location"]
            start = data["begin"]
            end = data["end"]
            date = data["onDate"]
            reserve_id = data["id"]
            print("已成功预约了座位{}，时间为{}~{}，日期为{}".format(location, start, end, date))
            return reserve_id
        else:
            print("座位预约失败，当前座位可能已被预约，或者您已经有有效预约！")

    #获取图书馆场馆的座位信息
    # def get_site_seat(self,reserve_site,reserve_seat):
    #     if reserve_site == "信息学部":
    #         url = "rest/v2/room/stats2/3"
    #         response_lib = self.req_with_json(url=url)
    #         data0 = response_lib["data"]
    #
    #         # 临时
    #         print(data0)
    #         a = ""
    #         for i in data0:
    #             p = []
    #             a = ""
    #             url = "rest/v2/room/layoutByDate/%s/%s" % (i["roomId"], self.reserve_date)
    #             response = self.req_with_json(url=url)
    #             data = response["data"]["layout"]
    #             for k in data:
    #                 m=[]
    #                 if data[k]["type"] == 'empty' or data[k]["name"] == "墙壁" or data[k]["name"] == "":
    #                     continue
    #                 elif data[k]["type"] =='seat':
    #                     seat_name = data[k]["name"]  # 返回给用户
    #                     seat_id = data[k]["id"]  # 获取座位id 目的达成！
    #                     # seat_status = data[k]["status"]
    #                     m.append(seat_name)
    #                     m.append(seat_id)
    #                     p.append(m)
    #             for n in p:
    #                 c = '''<option value='%s %s'>%s</option>'''%(n[0],n[1],n[0])
    #                 a += c
    #             d = '''
    #                     if (site.value=="%s"){
    #                         $("[name='seat']").html("%s");
    #                     }
    #                     ''' % (i["room"], a)
    #             print(d, end="")

        # if reserve_site =="信息学部":
        #     url="rest/v2/room/stats2/1"
        #     response_lib=self.req_with_json(url=url)
        #     data=response_lib["data"]
        #     for i in data:
        #         if reserve_seat==i["room"]:
        #             roomId=str(i["roomId"])
        # m=[]
        # url = "rest/v2/room/layoutByDate/%s/%s" % (roomId,self.reserve_date)
        # response = self.req_with_json(url=url)
        # data = response["data"]["layout"]
        # for i in data:
        #     if data[i]["type"] == 'empty':
        #         continue
        #     else:
        #         seat_name = data[i]["name"]  # 返回给用户
        #         seat_id = data[i]["id"]  # 获取座位id 目的达成！
        #         seat_status = data[i]["status"]
        #         m.append(seat_name)
        #         print(seat_name, seat_id,seat_status)  # 给用户返回seat_name，而后端使用id




    def stop_using(self):
        """
        用于释放座位
        {"status":"success","data":null,"message":"已终止使用当前预约","code":"0"}
        :return: dict
        """
        url = "rest/v2/stop"
        response = self.req_with_json(url)
        print(response["message"])
        if response["status"] != "success":
            return False
        return True

    def cancel_seat(self, reserve_id):
        """
        取消预约
        须先通过get_resevation_info函数获得座位的id
        {'status': 'success', 'data': None, 'message': '', 'code': '0'}
        :param reserve_id: int
        :return: True/False
        """
        url = "rest/v2/cancel/{}".format(reserve_id)
        response = self.req_with_json(url)
        if response["status"] == "success":
            print("取消预约成功")
            return True
        print("取消预约失败，请重试")
        return False

#1）从数据库里面获取数据 2）设置定时执行 3）异步进行（并考虑ip代理？）4）查询功能？查看座位对应的id？进行一下匹配？
def main(name,password,seatid,begintime,endtime):
    id=0
    #mine={}
    mine={'username':'%s'%name,'password':'%s'%password}
    order=AppRes(mine) #自带login，不用再额外登录login了
    order.get_resevation_info()
    #order.get_site_seat("信息学部","3C创客双屏电脑")
    id=order.reserve_seat(seatid,begintime,endtime) #替换
    print("预约data:",order.reserve_date)
    return id

def time_transfer(set_time):
    """
    将“小时：分钟”表示的时间转换为分钟表示
    :param set_time: str like {}:{}
    :return: str，minute
    """
    hours, minutes = [int(time_element) for time_element in set_time.split(":")]
    return hours * 60 + minutes

def sql():
    con = sqlite3.connect(r"E:\program\whulib\data.sqlite")
    cur = con.cursor()
    sql = "select * from users"
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    seatId=data[0][3]
    start_time = time_transfer(data[0][5])
    end_time = time_transfer(data[0][6])

    cur.close()
    con.close()
    return start_time,end_time,seatId
if __name__ == "__main__":

    while 1:
        localtime=time.localtime()
        print(localtime)
        #设置等待时间时间
        reserver_time=utils.get_reserve_date()[0]+" 22:30"
        #reserver_time="2021-05-09 22:43"
        print("reserver_time: ",reserver_time)
        reserver_time = datetime.datetime.strptime(reserver_time, "%Y-%m-%d %H:%M")
        now_time=datetime.datetime.now()
        sleep_time=(reserver_time-now_time).seconds
        print("sleep_time: ",sleep_time)
        time.sleep(sleep_time)
        while localtime[3]==22:
            time.sleep(40)
            localtime = time.localtime()
            print("sleeping1……")
            if localtime[3]==22 and localtime[4]==44: #在这里先获取token？
                while True:
                    time.sleep(0.5)
                    print("sleeping2……")
                    localtime = time.localtime()
                    if localtime[3]==22 and localtime[4]==45:
                        success_order=main("2018301040124","17071X",9208,480,1350)
                        print(success_order)
                        if success_order:
                            break
                        else:#更换第二个座位选项
                            success_order=main("2018301040124", "17071X", 9196, 480, 1350)
                            if success_order:
                                break
                            else:#更换第二个座位选项
                                main("2018301040124", "17071X", 9202, 480, 1350)








