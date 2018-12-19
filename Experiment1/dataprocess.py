import pymysql
import re
import codecs
import csv
import json
import os


def jiexin_wan(str):
    if str[-1] == '万':
        str = str[:-1]
        return int(float(str)*10000)
    if str == '--':
        return 0
    return int(str)


def getLabel(name):
    pat = re.compile(r'\【(.*?)\】')
    return pat.findall(name)


def getName(name):
    # 【Sp】3月的狮子Sp01【物语系列圈字幕组】
    name = name.replace('3月的狮子','三月的狮子')
    name = name.replace('100','一百')
    name = name.replace('之2','之二')
    if name[0] == '【'or name[0] == '[' or name[0] == '〔':
        pat = re.compile(r'[\】|\]|\〕](.*?)[\d|\【|\(|\〔|\[]')
        result = pat.findall(name)
        # 【7月】【熟肉/720P】蜘蛛侠S02E07【Classic字幕组】
        # 【TVB粤语】哆啦A梦新番(2018.08.20)怪盗大雄&戴小鸟帽一飞冲天【HDTVRip/1080p】【繁中字幕】
        # if name.count('【') > 2 and len(result) != 0:
        #     result = [result[1]]
        # 【生肉】机器人少女Z BDBOX特典
        if len(result) == 0:
            pat = re.compile(r'[\】|\]](.*)')
            result = pat.findall(name)

    else:
        # 深渊传说 SP01-02【华盟字幕】【480p】
        pat = re.compile(r'(.*?)[\d|\【|(]')
        result = pat.findall(name)
        return [result[0]]
        #[银光字幕组][七月新番★][漫威未来复仇者][26][简日双语][HDrip]
    if len(result) == 0 or ''.join(result) == '':
        if name.count('[') >= 5:
            pat = re.compile(r'\[(.*?)\]')
            result = pat.findall(name)
            return [result[2]]
        else: return [name]
    else: return result


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def getIndex(name):
    result = re.sub(r'\【(.*?)\】',"",name)
    result = re.sub(r'\((.*?)\)','',result)
    result = re.sub(r'\（(.*?)\）','',result)
    result = re.sub(r'\〔(.*?)\〕','',result)
    result = re.sub(r'\[(.*?)\]','',result)
    result = re.sub(r'\「(.*?)\」','',result)
    index = -1
    result = result[::-1]
    # 先找到第一个数字
    for i in range(0,len(result)):
        if is_number(result[i]):
            index = i
            break
    # 如果完全没有找到数字就返回
    if index == -1:
        return '-'
    else:
        ji = []
        duan = -1
        for i in range(index, len(result)):
            duan = i
            if is_number(result[i]) or result[i] == '-':
                ji.extend(result[i])
            else:
                break
        str = []
        # 再检查一下剩下的字符串中会不会有第*集这样的出现
        for i in range(duan, len(result)):
            if result[i] == '集' and is_number(result[i+1]):
                str = result[i+1:]
                break
        # 如果有，重新再找
        if len(str):
            reji = []
            for i in range(0, len(str)):
                if is_number(str[i]):
                    reji.append(str[i])
                else: return reversed(reji)
    return reversed(ji)


def processName(name):
    # name = name.replace('I','第一季')
    # 放在II上面
    name = name.replace('III','第三季')
    name = name.replace('II','第二季')
    name = name.replace('Ｘ','X')
    name = name.replace('#','')
    name = name.replace('「','')
    name = name.replace('」', '')
    name = name.replace('《','')
    name = name.replace('》','')
    name = name.replace('新番','')
    name = name.replace('四牌士','')
    name = name.replace('最终话','')
    name = name.replace('-','')
    name = name.title()
    name = name.replace(' ','')
    if name[-1] == '第' or name[-1] == '。' or name[-1] == '.' or name[-1] == '（'  or name[-1] == '/':
        name = name[:-1]
    if name.find('集') != -1:
        index = int(name.rfind('第'))
        name = name[0:index]
    return name


def get_conn():
     db = pymysql.connect('localhost',
                          'root',
                          '1234',
                          'biliuser',
                          charset='utf8')  # 连接数据库，如果不加charset，可能会导致乱码出现
     return db


def insert(db, i):
    cursor = db.cursor()
    sql = "select * from bilibili%s" % i
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            # label处理
            label = getLabel(row[0])
            label = '-'.join(label)
            # 集数
            ji = getIndex(row[0])
            ji = ''.join(ji)
            # name 处理
            name = getName(row[0])
            name = ''.join(name).strip()
            name = processName(name)
            play = jiexin_wan(row[1])
            DM = jiexin_wan(row[2])
            print(" name:{}  ".format(name))
            # insert = "insert into BILI(ANIME,LABEL,PLAY,DM,PLAY_MONTH,JI) VALUES(%s,%s,%s,%s, %s,%s);"
            # cursor.execute(insert,(name,label,play,DM,i,ji))
            # db.commit()
    except:
        raise Exception
        db.rollback()

    db.close()


def getTV(filename, sql, type = 'csv'):
    db = get_conn()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchmany(10)
        if type == 'csv':
            with codecs.open(filename=filename, mode='w', encoding='utf-8') as f:
                write = csv.writer(f, dialect='excel')
                write.writerow(i[0] for i in cursor.description)
                for row in results:
                    write.writerow(row)
        else:
            json_result = []
            for row in results:
                dict = {}
                dict['tv'] = row[0]
                dict['play'] = str(row[1])
                json_result.append(dict)
            print(json_result)
            with open(filename, 'w') as f:
                f.write(json.dumps(json_result,sort_keys=False, indent=4, separators=(',',':'), ensure_ascii=False))
    except:
        raise Exception
    db.close()

# 获得前几的集数
def getTV_Top(dir,sql):
    db = get_conn()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchmany(5)

        for row in results:
            name = row[0]
            sql2 = "select ANIME , play, dm , JI  from BILI where ANIME = '%s' " % name
            cursor.execute(sql2)
            play_top = cursor.fetchall()
            json_results = []
            for row in play_top:
                dict_results = {}
                dict_results['tv'] = name
                dict_results['play'] = row[1]
                dict_results['dm'] = row[2]
                dict_results['ji'] = row[3]
                json_results.append(dict_results)
                filename = os.path.join(dir, name+'.json')
            with open(filename,'w') as f:
                f.write(json.dumps(json_results,sort_keys=False, indent=4, separators=(',',':'),ensure_ascii=False))
    except: raise Exception
    db.close()

def getTop(filename,sql):
    db = get_conn()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchmany(10)
        json_result = []
        for row in results:
            dict = {}
            dict['tv'] = row[0]
            dict['play'] = str(row[1])
            json_result.append(dict)
        print(json_result)
        with open(filename, 'w') as f:
            f.write(json.dumps(json_result, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))
    except:
        raise Exception
    db.close()


def query_all(cur, sql, args):
    cur.execute(sql, args)
    return cur.fetchall()


def read_mysql_to_csv(filename):
    with codecs.open(filename=filename, mode='w', encoding='utf-8') as f:
        write = csv.writer(f, dialect='excel')
        conn = get_conn()
        cur = conn.cursor()
        sql = 'select * from BILI'
        results = query_all(cur=cur, sql=sql, args=None)
        for result in results:
            print(result)
            write.writerow(result)


def read_csv(file):
    csv_row = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            csv_row.extend([{title[i]:row[title[i]] for i in range(len(title))}])
        return csv_row


def write_json(data,json_file):
    with open(json_file,'w') as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',',':'), encoding="utf-8", ensure_ascii=False))


if __name__ == '__main__':

    # read_mysql_to_csv('bili.csv')

    for i in range(1,11):
        insert(get_conn(),i)

    # sql = 'select ANIME as tv ,SUM(PLAY) as play from BILI Group by ANIME order by play desc'
    # getTV_Top('play&dm_Top5_ji',sql)
    # getTV('bili-play.csv',sql)
    #
    # sql = 'select ANIME as tv ,SUM(DM) as dm from BILI Group by ANIME order by dm desc'
    # getTV('bili-dm.csv', sql)

    # for i in range(1,11):
    #     sql = 'select ANIME as tv, SUM(DM) as dm FROM BILI where play_month = %s GROUP BY tv order by dm desc' % i
    #     getTV('dmTop10_month/json/bili-dmTop10_month%s.json' % i, sql, 'json')
    #     getTV('dmTop10_month/csv/bili-dmTop10_month%s.csv' % i, sql, 'csv')





