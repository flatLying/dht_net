# coding=gbk
import mysql.connector
from flashtext import KeywordProcessor
import json
import os

'''
��Ҫ���һ������������൱�����������������������������������Դ����
'''

'''
����Ҫ����ÿ���ļ���ƥ��ٷֱ�Ϊ���٣�Խ��˵��ԽΣ��
Ȼ�󽫽���洢��ƥ��Ȱٷֱ����ݱ��У�����ƥ��ĵ����дʺ�λ����Ϣȫ�Ž�ȥ
'''

'''
֮����оۼ�ƥ���������ÿ����ͬ��IP�ļ��İ�ȫ������½�һ�ű���ȥ     
���ļ���������ƫ�࣬��mp4������txt�ȵ�
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

# ��ȡ���д��б�
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


# ƥ��һ���ļ�
def matching_filename(filename):
    keyword_processor = KeywordProcessor()
    for s in sen_list:
        keyword_processor.add_keyword(s)
    keywords_found = keyword_processor.extract_keywords(filename, span_info=True)
    print(keywords_found)
    return keywords_found


# ƥ�������ļ�
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

        # ����key�����İٷֱ�
        contain_len = len(key_find)

        # �õ�key�ĸ���
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
    ���ļ����γ����£��Ա��ں�������۴�Ƶ����
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
            # ȥ���ļ���׺
            name = os.path.splitext(i)[0]
            f.write(name)


'''
�����������ķ������ı��ؼ����������
'''


def public_sentiment():
    pass





def IP_analyse():
    '''
    ���IP��nodeID���о������
    IP �Ľ����ȶ���Ϊ�յ���ÿ���ļ��Ĳ���ضȵ��ܺ͵�ƽ��ֵ
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
        if dict_ip.get(i[1]):  # ����������ֵ
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
    ����port�ľ������
    port�Ĳ����������յ����ļ��Ĳ������ȵ��ܺ�
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
        if dict_port.get(i[1]):  # ����������ֵ
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
    �����ļ������ͽ��о��������ƥ��
    '''
    pass


# read_sen_list()
# matching_all_file()
# generate_file_article()
IP_analyse()
port_analyse()
