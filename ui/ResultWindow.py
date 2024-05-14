from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QStyle, QMessageBox


class Ui_MainWindow(object):
    def setupUi(self, ResultWindowV2):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        ResultWindowV2.setObjectName("MainWindow")
        ResultWindowV2.resize(1092, 866)
        self.centralwidget = QtWidgets.QWidget(ResultWindowV2)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 30, 41, 21))
        self.label.setObjectName("label")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(130, 30, 42, 22))
        self.spinBox.setObjectName("spinBox")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(400, 30, 71, 21))
        self.label_4.setObjectName("label_4")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(280, 30, 111, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(180, 30, 101, 21))
        self.label_3.setObjectName("label_3")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(80, 80, 931, 631))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QVideoWidget(self.verticalLayoutWidget)
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(80, 730, 931, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        # 设置按钮风格
        self.pushButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(520, 30, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        # 进度条
        self.horizontalSlider = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setRange(0, 0)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout.addWidget(self.horizontalSlider)
        ResultWindowV2.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ResultWindowV2)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1092, 23))
        self.menubar.setObjectName("menubar")
        ResultWindowV2.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ResultWindowV2)
        self.statusbar.setObjectName("statusbar")
        # self.statusBar.setFont(QFont("Noto Sans", 7))
        # self.statusBar.setFixedHeight(14)
        ResultWindowV2.setStatusBar(self.statusbar)

        self.retranslateUi(ResultWindowV2)
        QtCore.QMetaObject.connectSlotsByName(ResultWindowV2)

        # 界面关闭事件，询问用户是否关闭
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出', "是否要退出该界面？",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 清除视频查询结果
            # self.widget.rem
            # self.widget.clearFocus()
            event.accept()
        else:
            event.ignore()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "查询检测视频"))
        self.label.setText(_translate("MainWindow", "查询第"))
        self.label_4.setText(_translate("MainWindow", "的检测过程"))
        self.comboBox.setItemText(0, _translate("MainWindow", "左手"))
        self.comboBox.setItemText(1, _translate("MainWindow", "右手"))
        self.comboBox.setItemText(2, _translate("MainWindow", "手机盒_1"))
        self.comboBox.setItemText(3, _translate("MainWindow", "手机盒_2"))
        self.comboBox.setItemText(4, _translate("MainWindow", "手机盒_3"))
        self.comboBox.setItemText(5, _translate("MainWindow", "手机盒_4"))
        self.comboBox.setItemText(6, _translate("MainWindow", "手机盒_5"))
        self.comboBox.setItemText(7, _translate("MainWindow", "手机盒_6"))
        self.comboBox.setItemText(8, _translate("MainWindow", "手机盒_7"))
        self.comboBox.setItemText(9, _translate("MainWindow", "手机盒_8"))
        self.comboBox.setItemText(10, _translate("MainWindow", "手机盒_9"))
        self.comboBox.setItemText(11, _translate("MainWindow", "手机盒_10"))
        self.comboBox.setItemText(12, _translate("MainWindow", "纸带"))
        self.comboBox.setItemText(13, _translate("MainWindow", "标签"))
        self.comboBox.setItemText(14, _translate("MainWindow", "胶带封装"))
        self.label_3.setText(_translate("MainWindow", "个中箱检测流程中"))
        self.pushButton.setText(_translate("MainWindow", ""))
        self.pushButton_2.setText(_translate("MainWindow", "查询"))
from PyQt5.QtMultimediaWidgets import QVideoWidget
