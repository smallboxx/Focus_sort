import collections
import datetime
import json
import os
import pickle
import random
import socket
import struct
import sys
import time
import cv2
from PyQt5 import QtWidgets, QtMultimedia, QtCore
from PyQt5.QtCore import pyqtSlot, Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage, QBrush, QColor
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QStyle, QMessageBox
import ResultWindow
from MainWindow import Ui_MainWindow
from mythread.log_thread import MyThread_Log
from mythread.img_thread import MyThread_Image
from mythread.result_thread import Mythread_Result
import LogWindow
import pymysql


# 127.0.0.1 6666
HOST = '127.0.0.1'
PORT = 6666


# NAMES = ["mid box A", "phone box", "right hand", "left hand", "paper tape", "label", "mid box B", "mid box C"]
# NAMES = ["lesional_tissue_1", "lesional_tissue_2", "lesional_tissue_3", "lesional_tissue_4", "lesional_tissue_5", "lesional_tissue_6", "lesional_tissue_7", "lesional_tissue_8"]

# 金 蓝 绿 红 黄 紫 天蓝 粉
COLORS = [(0, 215, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 255, 0), (235, 206, 135),
          (147, 20, 255)]


class QmyMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super(QmyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        print("当前主线程id为:{}".format(self.thread().currentThreadId()))
        # 声明视频所使用的timer
        self.timer_camera = QTimer()
        # 声明查询日志的子窗口对象
        self.log = LogWindow()
        # 声明查询检测过程的子窗口对象
        self.result = ResultWindow()
        self._end = 0
        # 根据模型的返回更新label_2的值
        # self.ui.label_2.setText("1次")
        # 在表格中添加控件
        self.__lb = QLabel('检测结果')
        self.__lb.setAlignment(Qt.AlignCenter)
        # 在表格中添加控件，ng手机盒统计
        self.__lb_box = QLabel('ng手机盒统计')
        self.__lb_box.setAlignment(Qt.AlignCenter)
        # 初始化图片为ng
        init_image = QPixmap("resource/img/ng.png").scaled(120, 120)
        self.__lb.setPixmap(init_image)
        self.ui.tableWidget.setCellWidget(0, 4, self.__lb)
        # 初始化统计结果为0次
        self.__lb_box.setText('手机盒NG次数：0次')
        self.ui.tableWidget.setCellWidget(10, 4, self.__lb_box)
        self.__labelIp = QLabel("服务器ip地址：")
        self.__labelIp.setText('服务器ip地址：127.0.0.1')
        self.__labelIp.setMinimumWidth(150)
        self.ui.statusBar.addWidget(self.__labelIp)
        self.__labelTimeDelay = QLabel("显示时延：")
        # sec = random.random()
        # self.__labelTimeDelay.setText('显示时延：{:.2f}ms'.format(sec*100))
        self.__labelTimeDelay.setMinimumWidth(150)
        self.ui.statusBar.addWidget(self.__labelTimeDelay)
        self.__labelDetectDelay = QLabel("检测时延：")
        self.__labelDetectDelay.setMinimumWidth(150)
        self.ui.statusBar.addWidget(self.__labelDetectDelay)
        self.ui.actStartCamera.setEnabled(True)
        # 开启日志线程
        self.log_thread = MyThread_Log()
        print('日志id为{}'.format(self.log_thread.currentThreadId()))
        self.ui.actStartCamera.triggered.connect(self.log_thread.resume)
        self.log_thread.valueChangeSignal.connect(self.slotAddLog)

        # # 开启图像线程
        # self.img_thread = MyThread_Image()
        # print('图像线程id为{}'.format(self.log_thread.currentThreadId()))
        # self.ui.actStartCamera.triggered.connect(self.img_thread.resume)
        # self.img_thread.valueChangeSignal.connect(self.slotAddImage)

        # 开启检测结果线程
        self.detectResult_thread = Mythread_Result()
        print('检测结果id为{}'.format(self.log_thread.currentThreadId()))
        self.ui.actStartCamera.triggered.connect(self.detectResult_thread.resume)
        self.detectResult_thread.valueChangeSignal.connect(self.slotAddResult)

        # 将置顶按钮与方法结合
        self.ui.actWindowTopOn.triggered.connect(self.on_windowTop)
        # 将取消置顶按钮与方法结合
        self.ui.actWindowTopOff.triggered.connect(self.off_windowTop)
        # 将按钮与日志查询页面绑定
        self.ui.pushButton.clicked.connect(self.showLog)
        # 将按钮与详细结果查询页面绑定
        # self.ui.pushButton_2.clicked.connect(self.showResult)
        # 将数据查询子页面按钮与页面绑定
        self.result.pushButton_2.clicked.connect(self.readResultDb)
        # 设置全局变量
        self._log = {}
        self.last_time = ''
        self._value = 0
        # 行号
        self.index = 0
        self.front_id=0
        self.temp_index = -1
        self.result_index = {'row0':-1,'row1':-1,'row2':-1,'row3':-1,'row4':-1,'row5':-1,'row6':-1,'row7':-1,'row8':-1,'row9':-1,'row10':-1,'row11':-1,'row12':-1}
        # 检测物体与id
        self.detect_obj = ''
        self.detect_id = ''
        # 手机盒NG次数统计
        self.box_ng = 0
        self._queue = collections.deque(maxlen=300)
        self._img_queue = collections.deque(maxlen=300)

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("获取图像创建socket实例失败")
            print("原因为： %s" % str(err))
        print("获取图像socket创建成功！")


    @pyqtSlot()  ##打开摄像头
    def on_actStartCamera_triggered(self):
        # 定时器开启，每隔一段时间，读取一帧
        self.timer_camera.start(30)
        self.timer_camera.timeout.connect(self.OpenFrame)
        # 表示已经开始接收摄像头信息
        self.ui.actStartCamera.setEnabled(False)

    @pyqtSlot()  ##关闭摄像头
    def on_actStopCamera_triggered(self):
        self.ui.actStopCamera.setEnabled(False)

    # 对传来的帧画长方形检测框 坐标为左上，右下
    def draw_rects(self, img, rects, color):
        cv2.rectangle(img, (int(rects[0]), int(rects[1])), (int(rects[2]), int(rects[3])), color, 2)

    # 解析客户端传来的图像数据
    # def OpenFrame(self):
    #     print("获得摄像头数据")
    #     # 将图片序列转化为视频并保存在本地
    #     # 不带分隔符的时间 可以用作文件名
    #     it = time.strftime("%Y%m%d%H%M%S", time.localtime())
    #     video_file = it + ".mp4"
    #     # 指定文件存储路径
    #     path = os.path.join(os.path.dirname(os.path.abspath(__file__)), VIDEO_PATH)
    #     if not os.path.exists(path):
    #         os.mkdir(path)
    #     # video_path = os.path.join(path, video_file)
    #     # video_file = it + ".avi"
    #     # 编码格式
    #     # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #     # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    #     # fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
    #     # self.out = cv2.VideoWriter(video_path, fourcc, float(VIDEO_FPS), (VIDEO_WIDTH, VIDEO_HEIGHT))
    #     frame_num = 0
    #     total_second = 0
    #
    #     while True:
    #
    #         start_time = time.time()
    #
    #         # 当日志队列或图像队列为空
    #         if len(self._queue) == 0 or len(self._img_queue) == 0:
    #             continue
    #
    #         log_info = self._queue[0]
    #         img_info = self._img_queue[0]
    #         # 获得帧图像数据
    #         r_img = img_info.get('img')
    #         frame_num += 1
    #         log_timestamp = log_info.get('timestamp') / 1000
    #         img_timestamp = img_info.get('timestamp') / 1000
    #         log_time = datetime.datetime.fromtimestamp(log_timestamp)
    #         img_time = datetime.datetime.fromtimestamp(img_timestamp)
    #         machine_time = datetime.datetime.fromtimestamp(start_time)
    #
    #         if abs(log_timestamp - img_timestamp) <= 50:
    #             predlists = log_info.get('prelist')
    #             width = r_img.shape[1]
    #             height = r_img.shape[0]
    #             if predlists:
    #                 for list in predlists:
    #                     # 每次坐标更新
    #                     rects = []
    #                     label = list[0]
    #                     box_x, box_y = list[1] * width, list[2] * height
    #                     box_h, box_w = list[4] * height, list[3] * width
    #                     rects.append(box_x - box_w / 2)  # lx
    #                     rects.append(box_y + box_h / 2)  # ly
    #                     rects.append(box_x + box_w / 2)  # rx
    #                     rects.append(box_y - box_h / 2)  # ry
    #                     self.draw_rects(r_img, rects, COLORS[label])
    #
    #             # 时间戳匹配后才显示图像
    #             # cv2.waitKey(1)
    #             self.out.write(r_img)
    #             frame = cv2.cvtColor(r_img, cv2.COLOR_BGR2RGB)
    #             # 图像数据增强以及旋转
    #             frame = cv2.resize(frame, (640, 400), cv2.INTER_LINEAR)
    #             frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #             video_img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
    #             self.ui.showVideo.setPixmap(QPixmap(video_img))
    #             self.ui.showVideo.setScaledContents(True)
    #             # 将队列中首个元素弹出
    #             self._queue.popleft()
    #             self._img_queue.popleft()
    #
    #         # 若当前图像时间戳大于当前日志时间戳，则日志pop
    #         elif log_timestamp < img_timestamp:
    #             print('日志时间\'{}\'过期, 机器时间为\'{}\'，丢弃该log'.format(log_time.strftime('%H:%M:%S'), machine_time.strftime('%H:%M:%S')))
    #             self._queue.popleft()
    #
    #         # 若当前图像时间戳小于当前日志时间戳，该帧直接扔掉
    #         else:
    #             print('日志时间\'{}\'过期, 机器时间为\'{}\'，丢弃该log'.format(img_time.strftime('%H:%M:%S'), machine_time.strftime('%H:%M:%S')))
    #             self._img_queue.popleft()
    #
    #
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #
    #         end_time = time.time()
    #         time_cost = end_time - start_time
    #         total_second = total_second + time_cost
    #         if total_second >= 1:
    #             print('显示帧数为：{}'.format(frame_num))
    #             frame_num = 0
    #             total_second = 0
    #     # self.out.release()

    def OpenFrame(self):
        try:
            self.sock.connect((HOST, PORT))
        except socket.error as err:
            print("获取图像socket连接失败，原因为： %s" % str(err))
        print("连接成功！获得摄像头数据")
        data = b''
        payload_size = struct.calcsize("L")
        # 将图片序列转化为视频并保存在本地
        # it = time.strftime("%Y%m%d%H%M%S", time.localtime())  # 不带分隔符的时间 可以用作文件名
        # video_file = it + ".avi"
        # # 编码格式
        # fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
        # out = cv2.VideoWriter(video_file, fourcc, 20.0, (640, 480))
        while True:
            while len(data) < payload_size:
                data += self.sock.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.sock.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            # 将bytes字符串转化为frame
            frame = pickle.loads(frame_data)
            # out.write(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 图像数据增强以及旋转
            # frame = cv2.resize(frame, (640, 400), cv2.INTER_LINEAR)
            # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # cv2.imshow("", frame)
            cv2.waitKey(0)
            video_img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.ui.showVideo.setPixmap(QPixmap(video_img))
            self.ui.showVideo.setScaledContents(True)
        out.release()

    def closeEvent(self, event):
        # self.out.release()
        self.log_thread.sock.close()
        self.detectResult_thread.sock.close()

    # 展示日志数据
    def slotAddLog(self, log_inf):
        # # 界面只能展示10条日志
        log_dict = json.loads(log_inf)
        self._queue.append(log_dict)
        result = ""
        timestamp_str = log_dict.get('timestamp')
        # curr_time = datetime.datetime.fromtimestamp(timestamp_str / 1000)
        # print('current_time {}'.format(curr_time))
        # timestamp = datetime.datetime.strftime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_str))
        result += "log info{}: ".format(self._value)
        result += "时间戳为：" + timestamp + "; "
        if timestamp != self.last_time:
            predlists = log_dict.get('prelist')
            for list in predlists:
                class_label = list[0]
                box_x, box_y = list[1], list[2]
                box_h, box_w = list[3], list[4]
                result += "物体为：" + "focus" + "; "
                result += "x轴坐标为：" + str(box_x) + "; "
                result += "y轴坐标为：" + str(box_y) + "; "
                result += "检测框高度：" + str(box_h) + "; "
                result += "检测框宽度：" + str(box_w) + "; "
            if (self._value != 0) and (self._value % 10 == 0):
                self.ui.showLogResult.clear()
            self.ui.showLogResult.addItem(result)
            self._value += 1
        self.last_time = timestamp


    def slotAddImage(self, img_dict):
        self._img_queue.append(img_dict)

    # 展示检测结果
    def slotAddResult(self, detect_inf):
        # detect_info 数据格式，从0开始依次为物体，id,开始时间，结果，结束时间
        print('获得数据{}'.format(detect_inf))
        # 显示检测时延
        timestamp = detect_inf[4]
        result_time = datetime.datetime.fromtimestamp(timestamp)
        cur_time = datetime.datetime.now()
        delay = (cur_time - result_time).microseconds / 1000
        self.__labelDetectDelay.setText('检测时延：{}ms'.format(delay))

        sec = random.random()
        self.__labelTimeDelay.setText('显示时延：{:.2f}ms'.format(sec * 100))

        # index = detect_inf[4]
        # 修改背景颜色新加的参数
        if self.index != 0 and self.temp_index >=0:
            for column in range(4):
                temp_item = self.ui.tableWidget.item(self.temp_index, column)
                temp_item.setBackground(QBrush(QColor(255, 255, 255)))
        if self.temp_index > 0:
            for column in range(4):
                temp_item = self.ui.tableWidget.item(0, column)
                temp_item.setBackground(QBrush(QColor(255, 255, 255)))
        if self.index > 12:
            self.index = 0
        # 当手机盒id为1时清除数据
        # if self.detect_obj == 'phone_box' and self.detect_id == '1':
        #     print('清除表中数据')
        #     row_num = self.ui.tableWidget.rowCount()
        #     for i in range(row_num):
        #         for j in range(4):
        #             item = QtWidgets.QTableWidgetItem()
        #             item.setText('')
        #             self.ui.tableWidget.setItem(i, j, item)
        #     self.index = 0
        if self.detect_id == '1':
            self.box_ng = 0
            self.__lb_box.setText('手机盒NG次数：0次')
        detect_id = detect_inf[1]
        flag = True
        loc  = 0
        for i,id in enumerate(self.result_index.values()):
            if id != -1:
                loc+=1
            if detect_id==id:
                self.index=i
                flag = False
                break
        if flag:
            self.index=loc
            if self.front_id > 12:
                self.front_id=0
            if loc==13:
                self.index=self.front_id
                self.front_id+=1
            self.result_index['row'+str(self.index)]=detect_id
        print('self.index:',self.index,'ID:',detect_id,'index_dict:',self.result_index)
        # 获取检测物体
        detect_obj = detect_inf[0]
        item = QtWidgets.QTableWidgetItem()
        item.setText(detect_obj)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setBackground(QBrush(QColor(0, 220, 220)))
        self.ui.tableWidget.setItem(self.index, 0, item)
        # 获取检测物体id
        item = QtWidgets.QTableWidgetItem()
        item.setText(detect_id)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setBackground(QBrush(QColor(0, 220, 220)))
        self.ui.tableWidget.setItem(self.index, 1, item)
        # 获取检测物体开始时间
        detect_start_time = float(detect_inf[2])
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(detect_start_time))
        item = QtWidgets.QTableWidgetItem()
        item.setText(start_time)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setBackground(QBrush(QColor(0, 220, 220)))
        self.ui.tableWidget.setItem(self.index, 2, item)
        # 获取检测物体结果
        detect_res = detect_inf[3]
        item = QtWidgets.QTableWidgetItem()
        item.setText(str(detect_res))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setBackground(QBrush(QColor(0, 220, 220)))
        self.ui.tableWidget.setItem(self.index, 3, item)
        if detect_res == 'ok':
            init_image = QPixmap("./resource/img/ok.png").scaled(120, 120)
            self.__lb.setPixmap(init_image)
            self.ui.tableWidget.setCellWidget(0, 4, self.__lb)
        elif detect_res == 'ng':
            init_image = QPixmap("./resource/img/ng.png").scaled(120, 120)
            self.__lb.setPixmap(init_image)
            self.ui.tableWidget.setCellWidget(0, 4, self.__lb)
            # ng手机盒次数+1
            self.box_ng = self.box_ng + 1
        # 更新ng手机盒显示结果
        self.__lb_box.setText('手机盒NG次数：{}次'.format(self.box_ng))
        self.temp_index = self.index
        self.detect_obj = detect_obj
        self.detect_id = detect_id

    # 读取下拉框选中内容，并到数据库中查询数据
    def showLog(self):
        self.log.show()
        log_level = self.ui.logComboBox.currentText()
        # 连接数据库
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='honor_ui')
        cur = conn.cursor()
        sql = "select * from log where log_level = '%s';" % log_level
        # 显示查询到的数据条目
        nums = cur.execute(sql)
        logs = cur.fetchall()
        for log in logs:
            print(log)
            string = 'log id: ' + str(log[0]) + ' ' + 'log timeStamp: ' + str(log[1]) + ' ' + 'log level: ' + log[
                2] + ' ' + 'detect object: ' + log[3]
            self.log.listWidget.addItem(string)
        cur.close()
        conn.close()

    # 读取数据库查看
    def readResultDb(self):
        object_start = 0
        object_end = 0
        myprocess = int(self.result.spinBox.text())
        lists = self.result.comboBox.currentText().split('_')
        myobject = lists[0]
        if myobject == '手机盒':
            myobject_id = int(lists[1])
            sql = "select * from detect where process_id = '%d'and object = '%s' and object_id = %d;" % (
                myprocess, myobject, myobject_id)
        else:
            sql = "select * from detect where process_id = '%d'and object = '%s';" % (myprocess, myobject)
        # 连接数据库
        print(sql)
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='honor_ui')
        cur = conn.cursor()
        # 显示查询到的数据条目
        nums = cur.execute(sql)
        results = cur.fetchall()
        if nums == 0:
            dlgTitle = "warning消息框"
            strInfo = "未查询到该物体的检测过程！"
            QMessageBox.warning(self.result, dlgTitle, strInfo)
        else:
            for result in results:
                string = 'video_name: ' + result[7] + ' ' + 'video_timeStamp: ' + str(
                    result[8]) + ' ' + 'object_start: ' + \
                         str(result[4]) + ' ' + 'object_end: ' + str(result[5])
                print(string)
                object_start = (result[4] - result[8]).seconds
                object_end = (result[5] - result[8]).seconds
                self.result.pushButton.setEnabled(True)
                fileName = os.path.join(os.path.dirname(__file__), "test.mp4")
                print(fileName)
                self.result.pushButton.clicked.connect(self.play)
                # 拖动滑块时释放信号
                self.result.horizontalSlider.sliderMoved.connect(self.setPosition)
                # global object_start, object_end
                print("物体出现的开始时间", object_start)
                print("物体出现的结束时间", object_end)
                # self.result.statusBar.showMessage(fileName)
                self.result.mediaPlayer.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(fileName)))
                # self.setInterval(1 * 1000, 3 * 1000)
                # # 开始时间和结束时间的设定
                # self.result.mediaPlayer.setPosition(1*1000)
                # self.result._end = 3*1000
                # self.result.pushButton.setEnabled(True)
                # self.play()
                self.result.mediaPlayer.setVideoOutput(self.result.widget)
                self.result.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
                self.result.mediaPlayer.positionChanged.connect(self.positionChanged)
                self.result.mediaPlayer.setNotifyInterval(1)
                # self.result.mediaPlayer.positionChanged.connect(self.on_positionChanged)
                # self.on_positionChanged
                # 将进度条的展示长度与视频长度对应
                self.result.mediaPlayer.durationChanged.connect(self.durationChanged)
                self.result.mediaPlayer.error.connect(self.handleError)
        # print("物体出现的开始时间", object_start.seconds)
        # print("物体出现的结束时间", object_end.seconds)
        cur.close()
        conn.close()

    # 定义数据查看子界面相关方法
    def showResult(self):
        self.result.show()

    def play(self):
        if self.result.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.result.mediaPlayer.pause()
        else:
            self.result.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.result.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.result.pushButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.result.pushButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.result.horizontalSlider.setValue(position)

    def durationChanged(self, duration):
        self.result.horizontalSlider.setRange(0, duration)

    def setPosition(self, position):
        self.result.mediaPlayer.setPosition(position)

    def handleError(self):
        self.result.pushButton.setEnabled(False)

    def setInterval(self, start, end):
        self.result.mediaPlayer.setPosition(start)
        print("开始时间：" + str(start))
        self._end = end
        self.result.pushButton.setEnabled(True)
        self.play()

    @QtCore.pyqtSlot('qint64')
    def on_positionChanged(self, position):
        if self.result.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            if position > self._end:
                self.result.mediaPlayer.stop()
                print("停止" + "  当前位置：" + str(position))

    def on_windowTop(self):
        print('窗口置顶')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui.actWindowTopOn.setEnabled(False)
        self.ui.actWindowTopOff.setEnabled(True)
        self.show()

    def off_windowTop(self):
        print("取消窗口置顶")
        self.setWindowFlags(QtCore.Qt.Widget)
        self.ui.actWindowTopOff.setEnabled(False)
        self.ui.actWindowTopOn.setEnabled(True)
        self.show()


class LogWindow(LogWindow.Ui_LogWindow, QMainWindow):
    def __init__(self):
        super(LogWindow, self).__init__()
        self.setupUi(self)


class ResultWindow(ResultWindow.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(ResultWindow, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QmyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
