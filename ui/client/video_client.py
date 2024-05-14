import cv2
import socket
import pickle
import struct

cap = cv2.VideoCapture(0)
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('127.0.0.1', 6666))
print("客户端连接成功！")

while True:
    ret, frame = cap.read()
    # 将frame格式的数据转化为bytes字符串
    data = pickle.dumps(frame)
    # print("转换后的数据", data)
    print(len(data))
    clientsocket.sendall(struct.pack("L", len(data)) + data)
