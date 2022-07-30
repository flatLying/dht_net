# -*- coding: UTF-8 -*-
import mysql.connector
from PySide2.QtGui import QStandardItem, QStandardItemModel, QPixmap
from PySide2.QtWidgets import QApplication, QMessageBox, QHeaderView
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets
from wordcloud import WordCloud
import matplotlib.pyplot as plt  # 绘图

from analyse_data import IP_analyse, port_analyse
from download_redis import download, upload
from gen_filetxt import gen_file
import re # 正则表达式库
import collections # 词频统计库
import numpy as np # numpy数据处理库
import jieba # 结巴分词
import wordcloud # 词云展示库
from PIL import Image # 图像处理库
import matplotlib.pyplot as plt # 图像展示库


myconfig = {
    'host': 'localhost',
    'user': 'root',
    'pwd': '200178heyang'
}


class menu():
    def __init__(self):
        self.ui = QUiLoader().load('main.ui')
        self.ui.crawler.clicked.connect(self.downloadNewMagnet)
        self.ui.keywords.clicked.connect(self.showKeywords)
        self.ui.pushButton_4.clicked.connect(self.showAlert)
        self.ui.btinfo.clicked.connect(self.showMagnetInfo)

    def downloadNewMagnet(self):
        mag=download()
        pass

    def back_from_key(self):
        self.window4 = menu()
        self.window4.ui.show()
        self.window3.close()

    def back_from_magnetinfo(self):
        self.window4 = menu()
        self.window4.ui.show()
        self.window2.close()

    def showKeywords(self):
        self.window3=QUiLoader().load('keywords.ui')
        self.window3.show()
        self.window3.add.clicked.connect(self.add_key)
        self.window3.delete_2.clicked.connect(self.delete_key)
        self.window3.pushButton.clicked.connect(self.back_from_key)
        self.ui.close()

        db = mysql.connector.connect(
            host=myconfig['host'],
            user=myconfig['user'],
            password=myconfig['pwd'],
            db='BTmagnet',
        )
        cursor = db.cursor()
        cursor.execute("select * from sen_word")
        result = cursor.fetchall()

        x = 0
        n = len(result)
        self.model = QStandardItemModel(n, 1)
        self.model.setHorizontalHeaderLabels(['sensitive words'])
        for i in result:
            y = 0
            for j in i:
                print(result[x][y])
                print(type(result[x][y]))
                item = QStandardItem(str(result[x][y]))
                self.model.setItem(x, y, item)
                # self.window2.tableWidget.setItem(x, y, QStandardItem(str(result[x][y])))
                y = y + 1
            x = x + 1
        self.window3.tableView.setModel(self.model)
        self.window3.tableView.setColumnWidth(0, 150)

    def add_key(self):
        add_info=self.window3.addline.text()
        db = mysql.connector.connect(
            host=myconfig['host'],
            user=myconfig['user'],
            password=myconfig['pwd'],
            db='BTmagnet',
        )
        cursor = db.cursor()
        cursor.execute(f"insert into sen_word values (\'{add_info}\')")
        db.commit()
        self.showKeywords()

    def delete_key(self):
        delete_info = self.window3.lineEdit_2.text()
        db = mysql.connector.connect(
            host=myconfig['host'],
            user=myconfig['user'],
            password=myconfig['pwd'],
            db='BTmagnet',
        )
        cursor = db.cursor()
        cursor.execute(f"delete from sen_word  where keywords = \'{delete_info}\'")
        db.commit()
        self.showKeywords()

    def back_from_alert(self):
        self.window12= menu()
        self.window12.ui.show()
        self.window11.close()

    def showAlert(self):
        self.window11= QUiLoader().load('alert.ui')
        self.window11.show()
        self.window11.pushButton.clicked.connect(self.back_from_alert)
        self.ui.close()

        warmlog = []  # 需要预警的内容
        bad_mag=[] # 不好的磁力
        db = mysql.connector.connect(
            host=myconfig['host'],
            user=myconfig['user'],
            password=myconfig['pwd'],
            db='BTmagnet',
        )
        cursor = db.cursor()
        cursor.execute("select magnet from magnet_info natural join file_contain_key where contain_percent > 0")
        result = cursor.fetchall()
        for i in result:
           bad_mag.append(i[0])

        lines = open(r"warmlog.txt", "r", encoding="gbk")
        i = 1
        for line in lines:
            magnet, nodeid, ip, port = line.split(',', 3)
            if magnet in bad_mag:
                warmlog.append(magnet)
                self.window11.textBrowser.append("<font color=\"#FF0000\">" + "alerting......"  + "</font> ")
                self.window11.textBrowser.append("<font color=\"#FF0000\">" + "磁力信息： " + magnet + "</font> ")
                self.window11.textBrowser.append("<font color=\"#FF0000\">" + "nodeid 信息： " + nodeid + "</font> ")
                self.window11.textBrowser.append("<font color=\"#FF0000\">" + "IP 信息： " + ip + "</font> ")
                self.window11.textBrowser.append("<font color=\"#FF0000\">" + "PORT 信息： " + port + "</font> ")
                self.window11.textBrowser.append('\n')

            else:
                self.window11.textBrowser.append("<font color=\"#0F0000\">" + "receiving......"  + "</font> ")
                self.window11.textBrowser.append("<font color=\"#0F0000\">" + "磁力信息： " + magnet + "</font> ")
                self.window11.textBrowser.append("<font color=\"#0F0000\">" + "nodeid 信息： " + nodeid + "</font> ")
                self.window11.textBrowser.append("<font color=\"#0F0000\">" + "IP 信息： " + ip + "</font> ")
                self.window11.textBrowser.append("<font color=\"#0F0000\">" + "PORT 信息： " + port + "</font> ")
                self.window11.textBrowser.append('\n')

        print(bad_mag)

    def only_ciping(self):
        # 读取文件
        fn = open('test1.txt')  # 打开文件
        string_data = fn.read()  # 读出整个文件
        fn.close()  # 关闭文件

        # 文本预处理
        pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')  # 定义正则表达式匹配模式
        string_data = re.sub(pattern, '', string_data)  # 将符合模式的字符去除

        # 文本分词
        seg_list_exact = jieba.cut(string_data, cut_all=False)  # 精确模式分词
        object_list = []
        remove_words = [u'的', u'，', u'和', u'是', u'随着', u'对于', u'对', u'等', u'能', u'都', u'。', u' ', u'、', u'中', u'在',
                        u'了',
                        u'通常', u'如果', u'我们', u'需要', u'[', u'/', u']', u'_', u'@', u'\\', u',', u'-']  # 自定义去除词库

        for word in seg_list_exact:  # 循环读出每个分词
            if word not in remove_words:  # 如果不在去除词库中
                object_list.append(word)  # 分词追加到列表

        # 词频统计
        word_counts = collections.Counter(object_list)  # 对分词做词频统计
        word_counts_top50 = word_counts.most_common(50)  # 获取前50最高频的词
        print(word_counts_top50)  # 输出检查
        return word_counts_top50

    def back_from_yuntu(self):
        self.window6 = menu()
        self.window6.ui.show()
        self.window5.close()

    def ciping_yuntu(self):
        self.window5=QUiLoader().load('wordFre_yuntu.ui')
        self.window5.show()
        self.window5.pushButton.clicked.connect(self.back_from_yuntu)
        self.window2.close()

        gen_file()
        fn_1 = 'test1.txt'
        all_vocabs = []
        with open(fn_1, 'r', encoding='gbk') as f:
            lines = f.readlines()
            for line in lines:
                words = line.strip().split()
                all_vocabs.extend(words)
        num_dict = {}
        for w in all_vocabs:
            if w not in num_dict.keys():
                num_dict[w] = 1
            else:
                num_dict[w] += 1
        num_dict = sorted(num_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        print(dict(num_dict))
        all_ws = []
        i = 0
        for k, v in dict(num_dict).items():
            if i < 30:
                all_ws.extend([k] * v)
            else:
                break
            i += 1
        # 以空格为单位分隔，处理为词云输入的文本形式
        text = " ".join(all_ws)
        wc = WordCloud(font_path="STZHONGS.TTF", background_color="white", width=3000, height=1500, max_words=100,
                       contour_width=10, contour_color='steelblue', collocations=False).generate(text)
        # 导入python默认的绘图工具
        # STZHONGS.TTF
        plt.imshow(wc, interpolation="bilinear")  # 显示图形
        plt.axis("off")  # 隐藏坐标轴
        # 将词云图导出到当前目录
        wc.to_file('wc_cn.png')

        cipingtop50=self.only_ciping()
        for i in cipingtop50:
            self.window5.textBrowser.append(str(i[0])+" : "+str(i[1]))

        pix = QPixmap('wc_cn.png')
        self.window5.label_2.setGeometry(400, 100, 650, 400)
        self.window5.label_2.setPixmap(pix)
        self.window5.label_2.setScaledContents(True)

    def back_from_match(self):
        self.window8 = menu()
        self.window8.ui.show()
        self.window7.close()

    def upload_cloud(self):
        db = mysql.connector.connect(
            host=myconfig['host'],
            user=myconfig['user'],
            password=myconfig['pwd'],
            db='BTmagnet',
        )
        cursor = db.cursor()
        cursor.execute("select magnet from magnet_info natural join file_contain_key where contain_percent > 0")
        result=cursor.fetchall()
        for i in result:
            print("bad magnet: ", i[0])
            upload(i[0])
        pass

    def matchInfo(self):
        self.window7= QUiLoader().load('matchInfo.ui')
        self.window7.show()
        self.window7.back.clicked.connect(self.back_from_match)
        self.window7.pushButton.clicked.connect(self.upload_cloud)
        self.window2.close()

        db = mysql.connector.connect(
            host=myconfig['host'],
            user=myconfig['user'],
            password=myconfig['pwd'],
            db='BTmagnet',
        )
        cursor = db.cursor()
        cursor.execute("select * from file_contain_key")
        result = cursor.fetchall()
        x = 0
        n = len(result)
        self.model = QStandardItemModel(n, 3)
        self.model.setHorizontalHeaderLabels(['id', 'key_contain_info', 'contain_percent'])
        for i in result:
            y = 0
            for j in i:
                print(result[x][y])
                print(type(result[x][y]))
                item = QStandardItem(str(result[x][y]))
                self.model.setItem(x, y, item)
                # self.window2.tableWidget.setItem(x, y, QStandardItem(str(result[x][y])))
                y = y + 1
            x = x + 1
        self.window7.tableView.setModel(self.model)
        self.window7.tableView.setColumnWidth(0, 40)
        self.window7.tableView.setColumnWidth(1, 300)
        self.window7.tableView.setColumnWidth(2, 200)

    def back_from_jvji(self):
        self.window10 = menu()
        self.window10.ui.show()
        self.window9.close()

    def jvji(self):
        self.window9=QUiLoader().load('jvji.ui')
        self.window9.show()
        self.window9.pushButton.clicked.connect(self.back_from_jvji)
        self.window2.close()

        ip_health=IP_analyse()
        port_health=port_analyse()

        x = 0
        n = len(ip_health)
        self.model = QStandardItemModel(n, 1)
        self.model.setHorizontalHeaderLabels(['IP health'])
        for i in ip_health:
            y = 0
            for j in i:
                print(ip_health[x][y])
                print(type(ip_health[x][y]))
                item = QStandardItem(str(ip_health[x][y]))
                self.model.setItem(x, y, item)
                # self.window2.tableWidget.setItem(x, y, QStandardItem(str(result[x][y])))
                y = y + 1
            x = x + 1
        self.window9.IPView.setModel(self.model)
        self.window9.IPView.setColumnWidth(0, 150)
        self.window9.IPView.setColumnWidth(1, 250)

        x = 0
        n = len(port_health)
        self.model2 = QStandardItemModel(n, 1)
        self.model2.setHorizontalHeaderLabels(['PORT health'])
        for i in port_health:
            y = 0
            for j in i:
                print(port_health[x][y])
                print(type(port_health[x][y]))
                item = QStandardItem(str(port_health[x][y]))
                self.model2.setItem(x, y, item)
                # self.window2.tableWidget.setItem(x, y, QStandardItem(str(result[x][y])))
                y = y + 1
            x = x + 1
        self.window9.tableView_2.setModel(self.model2)
        self.window9.tableView_2.setColumnWidth(0, 150)

    def showMagnetInfo(self):
        self.window2 = QUiLoader().load('magnet_info.ui')
        self.window2.show()
        self.window2.pushButton_4.clicked.connect(self.back_from_magnetinfo)
        self.window2.ciping.clicked.connect(self.ciping_yuntu)
        self.window2.keywords_fenxi.clicked.connect(self.matchInfo)
        self.window2.jvji_fenxi.clicked.connect(self.jvji)

        self.ui.close()

        db = mysql.connector.connect(
            host=myconfig['host'],
            user=myconfig['user'],
            password=myconfig['pwd'],
            db='BTmagnet',
        )
        cursor = db.cursor()
        cursor.execute("select * from magnet_info")
        result = cursor.fetchall()
        x = 0
        n=len(result)
        self.model=QStandardItemModel(n, 6)
        self.model.setHorizontalHeaderLabels(['id', 'nodeid', 'ip', 'port', 'magnet', 'file_info'])
        for i in result:
            y = 0
            for j in i:
                print(result[x][y])
                print(type(result[x][y]))
                item=QStandardItem(str(result[x][y]))
                self.model.setItem(x,y,item)
                # self.window2.tableWidget.setItem(x, y, QStandardItem(str(result[x][y])))
                y = y + 1
            x = x + 1
        self.window2.tableView.setModel(self.model)
        self.window2.tableView.setColumnWidth(0, 40)
        self.window2.tableView.setColumnWidth(1, 500)
        self.window2.tableView.setColumnWidth(2, 200)
        self.window2.tableView.setColumnWidth(3, 200)
        self.window2.tableView.setColumnWidth(4, 800)
        self.window2.tableView.setColumnWidth(5, 1000)


app = QApplication([])
stats = menu()
stats.ui.show()
app.exec_()
