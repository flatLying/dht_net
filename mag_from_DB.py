import mysql.connector

myconfig={
    'host':'localhost',
    'user':'root',
    'pwd':'200178heyang'
}

db = mysql.connector.connect(
        host=myconfig['host'],
        user=myconfig['user'],
        password=myconfig['pwd'],
        db='BTmagnet',
    )
cursor = db.cursor()

def cloud2txt():
    lines = open(r"result.txt", "r", encoding="utf-8")
    i=1
    with open(r"测试数据.txt", "w+") as f:
        for line in lines:
            magnet,nodeid,ip,port=line.split(',',3)
            f.write(magnet + "\n")

cloud2txt()
