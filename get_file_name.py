import requests
import re
import mysql.connector
import linecache
import json
from pymysql.converters import escape_string

myconfig = {
    'host': 'localhost',
    'user': 'root',
    'pwd': '200178heyang'
}

db = mysql.connector.connect(
    host=myconfig['host'],
    user=myconfig['user'],
    password=myconfig['pwd'],
    db='BTmagnet',
)
cursor = db.cursor()

url = "https://pan.baidu.com/rest/2.0/services/cloud_dl?clienttype=0&app_id=250528&web=1&dp-logid=34289100544269710039&bdstoken=d48d684aa2bd18f590f3d3c2f4a48b50"
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "utf-8, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "140",
    "Content-Type": "application/x-www-form-urlencoded",
    "cookie": "BIDUPSID=05F6A4C225D8E0744919434114115D27; PSTM=1590634243; __yjs_duid=1_ca20fc02e8e5f8a44cd25e801a28ad701620137314040; secu=1; pan_login_way=1; PANWEB=1; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1648650370; BDCLND=j66qrZf%2Bsri%2F6T2hTUPaXJUxsofEFCGWOncLG1kgMVw%3D; BDUSS=EtVa3lmSGFLT0g5TnZhUEZPM1BxNEFxTFg5YmxvbzZEQllkdGZIZWtOSm9rWlJpRVFBQUFBJCQAAAAAAAAAAAEAAAB3xU32vqG~7L6hv-wzMQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGgEbWJoBG1iN; BDUSS_BFESS=EtVa3lmSGFLT0g5TnZhUEZPM1BxNEFxTFg5YmxvbzZEQllkdGZIZWtOSm9rWlJpRVFBQUFBJCQAAAAAAAAAAAEAAAB3xU32vqG~7L6hv-wzMQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGgEbWJoBG1iN; STOKEN=68461ab4d0bd5d81214c9321ab19ba478defe84bbb3d5f7e2c9e792cde76db79; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1648870299,1651311661,1651373304; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; delPer=0; PSINO=1; BAIDUID_BFESS=6F2887003A431B7062227F8532C7D386:SL=0:NR=10:FG=1; BA_HECTOR=a58g048524ag8l8l831h7v3oe0r; H_PS_PSSID=36425_36367_34812_36424_36165_34584_35978_36055_36267_36232_26350; csrfToken=kD-0FcPrnCMEG1jFRPPQzPsW; ndut_fmt=38D3967608BDB867D8E9F23A09BFDB92E89910EEF581D986F07EBA98D23F9BC6; ab_sr=1.0.1_YzM1NmYwZjcxODIzMGFmMDc2ZjQ5N2I3MjdkM2Y5NzQzMDY0MmI1YTVhOTRkZWQ1YzI4MTA1MzUwOGJkNmE2NzM5OWI3OGUwOTJhYjg3MGZkNmNhNTVkYjkzZWRhY2MzNWQ0MzViMWU0YzIyNTAwZmVkNzJlNWU5NTI0YWRiNzhkNGEyOTlhMDI5NzYwNDI2ZTJkNWMxYTQ1MTI3ZGUzOA==; PANPSC=10700162210421959865%3ADJI9ZdfpjgLjkQ9gKJ%2FAmEYemHfSgA%2FTjkmg96LDZiCgPH316bSxinOuad3EUeu5qkU5pdWuQ%2FY4Dr4ce1yIVyVnCRpnVR%2FnppETiI3L6kRQ64X1s1W05bCrPjRaYH4S%2FeSTN7pDPHui%2BY1X7udr9G2gud9gLjYtpqvB0tQPnfltcQe%2BbgwEaTCo8bcT1HMK; BAIDUID=0664E7425E7C3CE11E173999E00573A0:FG=1; AB_EXPERIMENT=%7B%22PC_SESSION_COOKIE_SWITCH%22%3A%22ON%22%2C%22group_cloud_smallflow%22%3A%22%22%2C%22ORDER_SIX_MONTH_CHECK%22%3A%22ON%22%2C%22group_smallflow%22%3A%22%22%2C%22CHROME80_SET_COOKIE%22%3A%22ON%22%2C%22group_smallflow_uri%22%3A%22%22%2C%22rccGetChannelInfoSink%22%3A%22ON%22%7D",
    "Host": "pan.baidu.com",
    "Origin": "https://pan.baidu.com",
    "Referer": "https://pan.baidu.com/disk/main?from=homeFlow",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


# 定义函数fun，根据磁力链接source_url,获取对应的文件名称
def fun(source_url, headers, f):
    data = {
        "method": "query_magnetinfo",
        "app_id": "250528",
        "source_url": source_url}
    try:
        r = requests.post(url, headers=headers, data=data)  # 发送请求
        # print(r.text)
        r.text[2:]
        file_name = eval(r.text[2:])["magnet_info"][0]["file_name"]
        print(file_name)
        f.write(file_name + "\n")
        return file_name
    except:
        file_name = "False"
        print(file_name)
        f.write(file_name + "\n")
        return file_name


def run(urls):
    with open(r"链接对应文件名.txt", "w+") as f:  # 将文件名和磁力链接逐行保存
        for source_url in urls:
            fun(source_url, headers, f)


def file_info2DB():
    lines = open(r"链接对应文件名.txt", "r", encoding="gbk")
    # lines2 = open(r"result.txt", "r", encoding="utf-8")
    i = 1
    for line in lines:
        if line[0:5] != "False":
            filename = 'result.txt'
            text = linecache.getline(filename, i)
            magnet, nodeid, ip, port = text.split(',', 3)
            port = port.replace("\n", "")
            info = line.replace("\n", "")
            es_info = escape_string(info)
            cursor.execute(
                f"insert into magnet_info(nodeid,ip,port,magnet,file_info) values (\'{nodeid}\',\'{ip}\',\'{port}\',\'{magnet}\',\'{es_info}\')")
        i = i + 1
    db.commit()


if __name__ == "__main__":
    # 读取磁力链接，生成urls磁力链接列表
    urls = []
    lines = open(r"测试数据.txt", "r", encoding="utf-8")
    for line in lines:
        # print(re.search(r"magnet\:.*", line)[0][:])
        try:
            urls.append(re.search(r"magnet\:.*", line)[0][:])
        except:
            pass

    # run(urls)
    # file_info2DB()

    '''
    第一件事：从result.txt中读取每一行的磁力，然后放到测试数据当中
    第二件事：将对应文件名中不是false的行的对应的result的信息也存在DB中
    '''
