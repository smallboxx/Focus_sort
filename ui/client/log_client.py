import os
import datetime
import json
import pickle
import time
import struct
from socket import *

IP = '127.0.0.1'
SERVER_PORT = 7777
dataSocket = socket(AF_INET, SOCK_STREAM)
dataSocket.connect((IP, SERVER_PORT))
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
    time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
    pred_dict = {'time': time_str, 'pred': predlist}
    pred_bytes = json.dumps(pred_dict).encode()
    data_len = len(pred_bytes)
    dataSocket.sendall(struct.pack('i', data_len))
    dataSocket.sendall(pred_bytes)
    # 序列化数据
    # data_bytes = pickle.dumps(pred_dict)
    # dataSocket.sendall(struct.pack('L', len(data_bytes)) + data_bytes)
    print("传输的数据为{}".format(pred_dict))
    time.sleep(0.2)
dataSocket.close()
