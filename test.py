# -*- coding: UTF-8 -*-
import sys

from PyQt5 import QtPrintSupport, QtGui
from PyQt5.QtCore import Qt, QMimeData, QDate, QDateTime, QTime
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtPrintSupport import QPageSetupDialog, QPrinter, QPrintDialog
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QFormLayout, QLabel, QLineEdit, QPushButton, QGridLayout, \
    QCalendarWidget, QVBoxLayout, QDateTimeEdit, QAction, QMainWindow, QTextEdit, QStatusBar, QFileDialog, QDialog, \
    QTableView




class TableViewDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置定位和左上角坐标
        self.setGeometry(300, 300, 460, 360)
        # 设置窗口标题
        self.setWindowTitle('QTableView表格视图控件 的演示')
        # 设置窗口图标
        # self.setWindowIcon(QIcon('../web.ico'))

        self.model = QStandardItemModel(4, 3)
        self.model.setHorizontalHeaderLabels(['id', '姓名', '年龄'])

        self.tableView = QTableView()
        # 关联 QTableView控件和Model
        self.tableView.setModel(self.model)

        # 添加数据
        item11 = QStandardItem('10')
        item12 = QStandardItem('打雷')
        item13 = QStandardItem('1000')
        self.model.setItem(0, 0, item11)
        self.model.setItem(0, 1, item12)
        self.model.setItem(0, 2, item13)

        item31 = QStandardItem('30')
        item32 = QStandardItem('下雨')
        item33 = QStandardItem('2000')
        self.model.setItem(2, 0, item31)
        self.model.setItem(2, 1, item32)
        self.model.setItem(2, 2, item33)

        layout = QVBoxLayout()
        layout.addWidget(self.tableView)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置应用图标
    app.setWindowIcon(QIcon('../web.ico'))
    w = TableViewDemo()
    w.show()
    sys.exit(app.exec_())