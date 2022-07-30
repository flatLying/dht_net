# coding=gbk
import mysql.connector
from flashtext import KeywordProcessor
import json
import os

'''
需要完成一个风向分析，相当于是舆情分析，看看那种类型是主流的资源需求
'''

'''
还需要计算每个文件的匹配百分比为多少，越高说明越危险
然后将结果存储在匹配度百分比数据表中，包括匹配的的敏感词和位置信息全放进去
'''

'''
之后进行聚集匹配操作，看每个相同的IP文件的安全情况，新建一张表存进去     
看文件内容那种偏多，是mp4，还是txt等等
'''

myconfig = {
    'host': 'localhost',
    'user': 'root',
    'pwd': '200178heyang'
}
sen_list = []
file = []
ip_health={}
sorted_ip_health={}
port_health={}
sorted_port_health={}

# 读取敏感词列表
def read_sen_list():
    db = mysql.connector.connect(
        host=myconfig['host'],
        user=myconfig['user'],
        password=myconfig['pwd'],
        db='BTmagnet',
    )
    cursor = db.cursor()
    cursor.execute("select keywords from sen_word")
    result = cursor.fetchall()
    for w in result:
        sen_list.append(w[0])


# 匹配一个文件
def matching_filename(filename):
    keyword_processor = KeywordProcessor()
    for s in sen_list:
        keyword_processor.add_keyword(s)
    keywords_found = keyword_processor.extract_keywords(filename, span_info=True)
    print(keywords_found)
    return keywords_found


# 匹配所有文件
def matching_all_file():
    db = mysql.connector.connect(
        host=myconfig['host'],
        user=myconfig['user'],
        password=myconfig['pwd'],
        db='BTmagnet',
    )
    cursor = db.cursor()
    cursor.execute("select file_info from magnet_info")
    result = cursor.fetchall()
    for w in result:
        file.append(w[0])

    for f in file:
        key_find = matching_filename(f)
        json_key_find = json.dumps(key_find)
        list_key_find = json.loads(json_key_find)

        # 计算key包含的百分比
        contain_len = len(key_find)

        # 得到key的个数
        cursor.execute("select count(*) from sen_word")
        result = cursor.fetchall()
        all_key_num = result[0][0]

        contain_percent = contain_len / all_key_num
        contain_percent = round(contain_percent, 5)
        print(contain_percent)

        cursor.execute(
            f"insert into file_contain_key(key_contain_info,contain_percent) values (\'{json_key_find}\',\'{contain_percent}\')")
    db.commit()


def generate_file_article():
    '''
    把文件名形成文章，以便于后面的舆论词频分析
    '''
    db = mysql.connector.connect(
        host=myconfig['host'],
        user=myconfig['user'],
        password=myconfig['pwd'],
        db='BTmagnet',
    )
    cursor = db.cursor()
    file2 = []
    cursor.execute("select file_info from magnet_info")
    result = cursor.fetchall()
    for w in result:
        file2.append(w[0])
    print(file2)

    with open(r"test1.txt", "w") as f:
        for i in file2:
            # 去掉文件后缀
            name = os.path.splitext(i)[0]
            f.write(name)


'''
这里进行舆情的分析，文本关键词主题分析
'''


def public_sentiment():
    pass





def IP_analyse():
    '''
    针对IP或nodeID进行聚类分析
    IP 的健康度定义为收到的每个文件的不监控度的总和的平均值
    '''
    db = mysql.connector.connect(
        host=myconfig['host'],
        user=myconfig['user'],
        password=myconfig['pwd'],
        db='BTmagnet',
    )
    cursor = db.cursor()
    cursor.execute(f"select id, ip from magnet_info")
    result = cursor.fetchall()
    dict_ip = {}
    for i in result:
        if dict_ip.get(i[1]):  # 如果有这个键值
            dict_ip[i[1]].append(i[0])
        else:
            dict_ip[i[1]] = [i[0]]
    for key,value in dict_ip.items():
        h_score=0
        for id_ip in value:
            cursor.execute(f"select contain_percent from file_contain_key where id = \'{id_ip}\' ")
            result=cursor.fetchall()
            h_score=h_score+result[0][0]
        h_score_aver=h_score/(len(value))
        ip_health[key]=h_score_aver
    sorted_ip_health = sorted(ip_health.items(), key = lambda kv:(kv[1], kv[0]),reverse = True)
    print(sorted_ip_health)
    return sorted_ip_health



def port_analyse():
    '''
    分析port的聚类分析
    port的不健康度是收到的文件的不健康度的总和
    :return:
    '''
    db = mysql.connector.connect(
        host=myconfig['host'],
        user=myconfig['user'],
        password=myconfig['pwd'],
        db='BTmagnet',
    )
    cursor = db.cursor()
    cursor.execute(f"select id, port from magnet_info")
    result = cursor.fetchall()
    dict_port = {}
    for i in result:
        if dict_port.get(i[1]):  # 如果有这个键值
            dict_port[i[1]].append(i[0])
        else:
            dict_port[i[1]] = [i[0]]
    for key,value in dict_port.items():
        h_score=0
        for id_port in value:
            cursor.execute(f"select contain_percent from file_contain_key where id = \'{id_port}\' ")
            result=cursor.fetchall()
            h_score=h_score+result[0][0]
        h_score_aver=h_score/(len(value))
        port_health[key]=h_score_aver
    sorted_port_health = sorted(port_health.items(),key = lambda x:x[1],reverse = True)
    print(sorted_port_health)
    return sorted_port_health


def file_type_analyse():
    '''
    对于文件的类型进行聚类分析，匹配
    '''
    pass


# read_sen_list()
# matching_all_file()
# generate_file_article()
IP_analyse()
port_analyse()
