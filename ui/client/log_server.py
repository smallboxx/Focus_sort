import datetime
import json
import pickle
import socket
import struct
import threading

# from test5.client.ReadYml import read_yaml

# HOST = read_yaml('ip1', 'address')
# PORT = read_yaml('ip1', 'port')
import time

names = ["lesional_tissue_1", "lesional_tissue_2", "lesional_tissue_3", "lesional_tissue_4", "lesional_tissue_5", "lesional_tissue_6", "lesional_tissue_7", "lesional_tissue_8"]


def listenToClient(server, address):
    while True:
        predlist = [[3, 0.4401041567325592, 0.4983333349227905, 0.11562500149011612, 0.14666666090488434],
                    [0, 0.7059895992279053, 0.5491666793823242, 0.4411458373069763, 0.5516666769981384],
                    [3, 0.4401041567325592, 0.4983333349227905, 0.11562500149011612, 0.14666666090488434]
            , [3, 0.4401041567325592, 0.4983333349227905, 0.11562500149011612, 0.14666666090488434],
                    [3, 0.4401041567325592, 0.4983333349227905, 0.11562500149011612, 0.14666666090488434],
                    [3, 0.4401041567325592, 0.4983333349227905, 0.11562500149011612, 0.14666666090488434]
            , [3, 0.4401041567325592, 0.4983333349227905, 0.11562500149011612, 0.14666666090488434],
                    [3, 0.4401041567325592, 0.4983333349227905, 0.11562500149011612, 0.14666666090488434]
            , [3, 0.4401041567325592, 0.4983333349227905, 0.11562500149011612, 0.14666666090488434],
                    [3, 0.4401041567325592, 0.4983333349227905, 0.11562500149011612, 0.14666666090488434]
            , [3, 0.4401041567325592, 0.4983333349227905, 0.11562500149011612, 0.14666666090488434],
                    [3, 0.4401041567325592, 0.4983333349227905, 0.11562500149011612, 0.14666666090488434]
            , [3, 0.4401041567325592, 0.4983333349227905, 0.11562500149011612, 0.14666666090488434],
                    [5, 0.4401041567325592, 0.4983333349227905, 0.11562500149011612, 0.14666666090488434]]
        curr_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S.%f')
        pred_dict = {'time': time_str, 'prelist': predlist}
        pred_bytes = json.dumps(pred_dict).encode()
        data_len = len(pred_bytes)
        server.sendall(struct.pack('i', data_len))
        server.sendall(pred_bytes)
        # 序列化数据
        # data_bytes = pickle.dumps(pred_dict)
        # dataSocket.sendall(struct.pack('L', len(data_bytes)) + data_bytes)
        print("传输的数据为{}".format(pred_dict))
        time.sleep(0.2)
    dataSocket.close()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("创建socket实例失败")
    print("原因为： %s" % str(err))
print("socket创建成功！")
try:
    # sock.bind((HOST, PORT))
    sock.bind(('127.0.0.1', 1123))
except socket.error as err:
    print("socket绑定端口失败，原因为： %s" % str(err))
# 设置监听端口的最大连接数
sock.listen(10)
while True:
    try:
        connect_info, ip_info = sock.accept()
        print("连接到主机： %s , 正在监听" % str(ip_info))
    except socket.error as err:
        print("socket连接指定主机失败, 原因为： %s" % str(err))
    # threading.Thread(target=listenToClient, args=(connect_info, ip_info)).start()
    recv = connect_info.recv(1024)
    print('接收客户端的数据{}'.format(recv))
    listenToClient(connect_info, ip_info)

