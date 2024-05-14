import pickle
import socket
import struct
import time

import cv2


# 解析客户端传来的图像数据
class ReadFrame:
    def __init__(self, connect):
        self.connect = connect

    def OpenFrame(self):
        print("获得摄像头数据")
        data = b''
        payload_size = struct.calcsize("L")
        # 将图片序列转化为视频并保存在本地
        it = time.strftime("%Y%m%d%H%M%S", time.localtime())  # 不带分隔符的时间 可以用作文件名
        video_file = it + ".avi"
        # 编码格式
        fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
        out = cv2.VideoWriter(video_file, fourcc, 20.0, (640, 480))
        while True:
            while len(data) < payload_size:
                data += self.connect.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += self.connect.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            # 将bytes字符串转化为frame
            frame = pickle.loads(frame_data)
            out.write(frame)
        out.release()
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("实时日志创建socket实例失败")
    print("原因为： %s" % str(err))
print("实时日志socket创建成功！")
try:
    # sock.bind((HOST, PORT))
    sock.bind(('127.0.0.1', 6666))
except socket.error as err:
    print("实时日志socket绑定端口失败，原因为： %s" % str(err))
# 设置监听端口的最大连接数
sock.listen(10)
connect, ip = sock.accept()
readFrame = ReadFrame(connect)
readFrame.OpenFrame()
