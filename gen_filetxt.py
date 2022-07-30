import requests
import re
import mysql.connector
import linecache
import json
from pymysql.converters import escape_string
import os


def gen_file():
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
    file = []

    cursor.execute("select file_info from magnet_info")
    result = cursor.fetchall()
    for w in result:
        file.append(w[0])
    print(file)

    with open(r"test1.txt", "w") as f:
        for i in file:
            name = os.path.splitext(i)[0]
            f.write(name)


gen_file()
