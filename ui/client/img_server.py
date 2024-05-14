import cv2
import socket
import pickle
import struct

cap = cv2.VideoCapture(0)
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("图像创建socket实例失败")
    print("原因为： %s" % str(err))
print("图像socket创建成功！")
try:
    # sock.bind((HOST, PORT))
    sock.bind(('127.0.0.1', 6666))
except socket.error as err:
    print("图像socket绑定端口失败，原因为： %s" % str(err))

sock.listen(10)

try:
    connect_info, ip_info = sock.accept()
    print("连接到主机： %s , 正在监听" % str(ip_info))
except socket.error as err:
    print("socket连接指定主机失败, 原因为： %s" % str(err))


while True:
    ret, frame = cap.read()
    # 将frame格式的数据转化为bytes字符串
    data = pickle.dumps(frame)
    # print("转换后的数据", data)
    print(len(data))
    # print(struct.pack("L", len(data)) + data)
    connect_info.sendall(struct.pack("L", len(data)) + data)
