import struct
from PyQt5.QtCore import QThread, pyqtSignal, QWaitCondition, QMutex
import socket

# 127.0.0.1 7777
HOST = '127.0.0.1'
PORT =  7777
UDP_PORT = ('127.0.0.1', 6666)

NAMES = ["mid box A", "phone box", "right hand", "left hand", "paper tape", "label", "mid box B", "mid box C"]


class MyThread_Log(QThread):
    valueChangeSignal = pyqtSignal(str)

    def __init__(self):
        super(MyThread_Log, self).__init__()
        self._isPause = True
        self._value = 1

        self.cond = QWaitCondition()
        self.mutex = QMutex()
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("实时日志创建socket实例失败")
            print("原因为： %s" % str(err))
        print("实时日志socket创建成功！")

    def pause(self):
        print("线程休眠")
        self._isPause = True
        print(self.currentThreadId())

    def resume(self):
        print("线程启动")
        self._isPause = False
        self.cond.wakeAll()
        self.start()

    def run(self):
        def listenToServer(server):
            print("接收日志server端数据....")
            # last_time = ''
            # 初始化缓冲区
            buffer = b''
            while True:
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
                # msg = json.loads(total_data.decode())
                self.valueChangeSignal.emit(total_data.decode())
        try:
            self.sock.connect((HOST, PORT))
        except socket.error as err:
            print("实时日志socket连接失败，原因为： %s" % str(err))
        # 传输本机ip以及udp的端口号
        net_info = str(UDP_PORT)
        self.sock.send(net_info.encode('utf-8'))
        print('已传输本机ip以及udp的端口号')
        listenToServer(self.sock)

