import pymysql
import pandas as pd
db = pymysql.connect('localhost',
                          'root',
                          '1234',
                          'biliuser',
                          charset='utf8')  # 连接数据库，如果不加charset，可能会导致乱码出现


def insert_db():
    i = pd.read_csv('用户表2.csv', engine='python',encoding='utf-8')
    list_all = i.values
    all_list = list(list_all)
    for i in all_list:
        # print(i[0], i[1],i[2])
        if check_up(i[0]) == 0:
            z = str(i[2])
            z = z.replace("\r\n", '')
            z = z.replace(" ", '')
            z = z.replace("\\", '')
            z = z.replace("/", '')
            z = z.replace("\"", '')
            z = z.replace("nan",'')
            print("{}存入简介: {}".format(i[0], z))
            cursor = db.cursor()
            insert1 = 'insert into Bi_User(ID,NAME,intro) values(%s,"%s","%s");' % (i[0],i[1], z)
            cursor.execute(insert1)
            db.commit()
        else:
            continue

def insert_follow():
    i = pd.read_csv('联系表2.csv', engine='python')
    id_list = i.values
    for i in id_list:
        if check_id(i[0],i[1]) == 0:
            cursor = db.cursor()
            print(i[0],i[1])
            insert = "insert into Bi_follow(follower, followed) values(%s,%s)" % (i[0],i[1])
            cursor.execute(insert)
            db.commit()

def check_id(id1,id2):
    try:
        cursor = db.cursor()
        select = "select * from Bi_follow where follower = %s and followed = %s" % (id1,id2)
        cursor.execute(select)
        count = cursor.rowcount
        return count
    except:
        return

def check_up(up_id):
    try:
        cursor = db.cursor()
        select = "select * from Bi_User where ID = %s" % up_id
        cursor.execute(select)
        count = cursor.rowcount
        return count
    except:
        print("检查此up是否已经搜果有无")
        return

def check_nan():
    try:
        cursor = db.cursor()
        select = "select * from Bi_User where intro = 'nan'"
        cursor.execute(select)
        result = cursor.fetchall()
        for row in result:
            cursor2 = db.cursor()
            print(row[0])
            delete = 'delete from Bi_User where id = %s' % row[0]
            cursor2.execute(delete)
            db.commit()
    except:
        db.rollback()
        return
if __name__ == '__main__':
    insert_db()