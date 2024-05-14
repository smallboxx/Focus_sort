import json
import socket
import struct
import time

from PyQt5.QtCore import QThread, pyqtSignal, QWaitCondition, QMutex


class Mythread_Result(QThread):
    valueChangeSignal = pyqtSignal(list)

    def __init__(self):
        super(Mythread_Result, self).__init__()
        self._isPause = True
        # self._value = 0
        self.num = 0

        self.cond = QWaitCondition()
        self.mutex = QMutex()
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("检测结果创建socket实例失败")
            print("原因为： %s" % str(err))
        print("检测结果socket创建成功！")

    def pause(self):
        print("线程休眠")
        self._isPause = True

    def resume(self):
        print("线程启动")
        self._isPause = False
        self.cond.wakeAll()
        self.start()

    def run(self):
        def listenToServer(server):
            print("接收检测结果server端数据....")
            last_time = ''
            # 初始化缓冲区
            buffer = b''
            while True:
                # if self._value > 10:
                #     self._value = 0
                # 初始化数据区
                total_data = b''
                    # 获取缓冲区长度
                buffer_len = len(buffer)

                # 缓冲区取值
                if buffer_len > 4:
                    data_len_bytes = buffer[:4]
                    buffer = buffer[4:]

                elif buffer_len > 0:
                    data_len_bytes = buffer + server.recv(4 - buffer_len)
                    buffer = b''
                else:
                    data_len_bytes = server.recv(4)

                buffer_len = len(buffer)

                # 长度为0说明连接已断开
                if len(data_len_bytes) == 0:
                    break

                # 获取数据长度
                data_len = struct.unpack('i', data_len_bytes)[0]

                # 若缓冲区长度小于数据长度，则需要从连接中字节流
                if buffer_len < data_len:
                    total_data += buffer
                    buffer = b''

                    while True:

                        total_data_len = len(total_data)
                            # 每次取1024字节
                        recv_data = server.recv(1024)

                            # 若本次接收后，大于所需数据长度，则按实际长度截断，剩余字节放入缓冲区
                        if (total_data_len + len(recv_data)) >= data_len:
                            total_data += recv_data[:data_len - total_data_len]
                            buffer += recv_data[data_len - total_data_len:]
                            break

                        # 若本次接收后仍然小于所需数据长度，则直接将接收部分放入数据区中
                        else:
                            total_data += recv_data

                # 若缓冲区长度大于所需数据长度，则直接从缓冲区取字节流
                else:
                    total_data += buffer[:data_len]
                    buffer = buffer[data_len:]

                # 数据反序列化
                # print(total_data)
                msg = json.loads(total_data.decode())
                # detect_info 数据格式，从0开始依次为物体，id,结果，行号
                # 前端界面展示的list格式为：['手机盒', '1','ok', 0]
                message = []
                print('获得的开始时间为{}， 结束时间为{}'
                      .format(time.strftime("%Y%m%d%H%M%S", time.localtime(msg['start'])), time.strftime("%Y%m%d%H%M%S", time.localtime(msg['end']))))
                print('获得的模型为'.format(msg['model']))
                # 获得检测物体
                message.append(msg['object'])
                # 获得检测id
                message.append(str(msg['id']))
                # 获得检测开始时间
                message.append(str(msg['start']))
                # 获得检测结果
                message.append(msg['result'])
                message.append(msg['end'])
                print("列表传输数据为：")
                print(message)
                # 添加行号
                # message.append(self._value)
                self.valueChangeSignal.emit(message)
                # self._value += 1

        try:
            self.sock.connect(('127.0.0.1', 8888))
        except socket.error as err:
            print("检测结果socket连接失败，原因为： %s" % str(err))
        net_info = '\'' + '127.0.0.1' + '\'' + ':' + str(8888)
        self.sock.send(net_info.encode('utf-8'))
        listenToServer(self.sock)
