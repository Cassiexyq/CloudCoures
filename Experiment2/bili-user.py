
import re
import pymysql
import random
import requests
from urllib import parse
import codecs
import csv
# import multiprocessing as mp


class Bilibili:
    def __init__(self):
        self.db = pymysql.connect('localhost',
                                  'root',
                                  '1234',
                                  'biliuser',
                                  charset='utf8')  # 连接数据库，如果不加charset，可能会导致乱码出现
        self.param = {
            'callback':'_jp6',
            'jsonp': 'jsonp',
            'order': 'desc',
            'pn':1,
            'ps':20
            # 'vmid':3231392
        }

        self.parm2 = {
            'csrf' : ''
        }

        self.headers ={
            'User-Agent':
         # 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Accept': '*/*',
            'Host':'api.bilibili.com',
            # 'Referer':'https://space.bilibili.com/3231392/',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

        self.header2 = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Accept':'pplication / json, text / plain, * / *',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection':'keep - alive',
            'Cotent-Length':'18',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'space.bilibili.com'
        }

    def create_Table(self):        #建表
        db = self.db
        cursor = db.cursor()
        table1 = "CREATE TABLE Bi_User(ID INT NOT NULL,NAME VARCHAR(255) NOT NULL,intro VARCHAR(255),PRIMARY KEY(ID))"
        table2 = "CREATE TABLE Bi_Follow(follower int NOT NULL, followed int NOT NULL, PRIMARY KEY(follower, followed))"
        cursor.execute(table1)
        cursor.execute(table2)
        db.commit()

    def check_up(self, up_id):
        try:
            db = self.db
            cursor = db.cursor()
            select = "select * from Bi_User where ID = %s" % up_id
            cursor.execute(select)
            count = cursor.rowcount
            return count
        except:
            print("检查此up是否已经搜果有无")
            return

    def insert_db(self, id_list, name_list, intro_list):      #插入方法
        try:
            db = self.db
            cursor = db.cursor()
            up_id = id_list[0]
            for x, y, z in zip(id_list, name_list,intro_list):
                select = "select * from Bi_User where ID = %s" % int(x)
                cursor.execute(select)
                count = cursor.rowcount
                # 当刚好是up的id且影响条数不为0
                if x == up_id and count != 0:
                    print("此up已经出现搜过了")
                    return
                if count == 0:
                    z = z.replace("\r\n",'')
                    z = z.replace(" ",'')
                    z = z.replace("\\",'')
                    z = z.replace("/",'')
                    z = z.replace("\"",'')
                    print("存入的简介："+z)
                    insert1 = 'insert into Bi_User(ID,NAME,intro) values(%s,"%s","%s");' % (x, y, z)
                    cursor.execute(insert1)
                    db.commit()
                if x != up_id:
                    insert2 = "insert into Bi_Follow(follower,followed) values(%s,%s);" % (up_id, x)
                    cursor.execute(insert2)
                    db.commit()
        except:
            db.rollback()
            raise Exception
            return

    def update_db(self):
        try:
            db = self.db
            cursor = db.cursor()
            select = "select * from Bi_user"
            cursor.execute(select)
            results = cursor.fetchall()
            for i in results:
                intro = i[2]
                print(i[1])
                # print('1: '+ intro)
                _id = i[0]
                # intro1 = intro.replace("\n","")
                # intro1 = intro1.replace('\\n','')
                intro1 = intro.replace("\r\n",'')
                # intro1 = intro1.replace(' ','')
                # # intro1 = intro1.strip()
                # print('2: '+intro1)
                update = "update Bi_User set intro = '%s' where ID = %s" % (intro1,_id)
                cursor.execute(update)
                db.commit()
        except:
            return

    def read_mysql_to_csv(self, filename):
        db = self.db
        with codecs.open(filename=filename, mode='w', encoding='utf-8') as f:
            write = csv.writer(f, dialect='excel')
            cur = db.cursor()
            sql = 'select * from Bi_follow'
            cur.execute(sql)
            results = cur.fetchall()
            for result in results:
                print(result)
                write.writerow(result)

    def main(self):
        header = self.headers
        head_port = self.header2
        parm = self.param
        parm_port = self.parm2
        for _ in range(5000):
            # i = 24459859
            # i = 472636
            i = random.randint(0,100000000)
            if bili.check_up(i) != 0:
                print("此up已经搜过")
                continue
            print(i)
            gz_name = []
            gz_id = []
            gz_into = []

            # 获得up名字和简介
            head_port['Referer'] = 'https://space.bilibili.com/%s/' % i
            parm_port['mid'] = i
            url_port = 'https://space.bilibili.com/ajax/member/GetInfo'
            url_request = requests.post(url_port,data=parm_port,headers=head_port)
            # 如果存在这个id
            print(url_request.status_code)
            if url_request.status_code == 200:
                up_info = url_request.content.decode('unicode_escape').replace('\n','')
                # print(up_info)
                status = re.findall('"status":(.*?),"',up_info)
                # print(status)
                if status[0] == 'false':
                    print("不存在该用户")
                    continue
                up_name = re.findall('"name":"(.*?)"',up_info)
                sign = re.findall('"sign":"(.*?)"', up_info)
                # print(sign)
                print("up:"+up_name[0])
                print("up 简介："+sign[0].replace(" ",''))
                # 把up信息存入
                gz_name.append(up_name[0])
                gz_into.append(sign[0].replace(" ",''))
                gz_id.append(i)

                # 获得up关注的列表
                gz_count = 0
                header['Referer'] = 'https://space.bilibili.com/%s/' % i
                parm['vmid'] = i

                for index in range(1, 6):
                    parm['pn'] = index
                    url = "https://api.bilibili.com/x/relation/followings?" + parse.urlencode(parm)
                    url_response = requests.get(url,params=parm,headers=header,stream = True)
                    result = url_response.content.decode('utf-8').replace('\n','')
                    if index == 1:
                        gz_count = re.findall('"total":(.*?)}', result)
                        gz_count = int(gz_count[0])
                        print("关注数：")
                        print(gz_count)
                    name = re.findall('"uname":"(.*?)",', result)
                    id_l = re.findall('"mid":(.*?),', result)
                    sign = re.findall('"sign":"(.*?)",', result)
                    # print(result)
                    gz_name.extend(name)
                    gz_id.extend(id_l)
                    gz_into.extend(sign)
                    if gz_count < 20:
                        break
                    if gz_count < 40 and index == 2:
                        break
                    if gz_count < 60 and index == 3:
                        break
                    if gz_count < 80 and index == 4:
                        break

                print("关注的名字列表：")
                print(gz_name[1:])
                print("关注的id列表：")
                print(gz_id[1:])
                # print("关注的简介列表：")
                # print(gz_into[1:])

                bili.insert_db(gz_id, gz_name,gz_into)

            else:
                continue

    def write_csv(self):
        try:
            db = self.db
            db
        except:
            return

if __name__ == '__main__':
    bili = Bilibili()
    bili.main()
    # bili.update_db()
    # bili.read_mysql_to_csv('关系表.csv')
