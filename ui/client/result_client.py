import json
import socket
import struct
import time

from ReadYml import read_yaml

# 127.0.0.1 8888
HOST = read_yaml('ip3', 'address')
PORT = read_yaml('ip3', 'port')


def client():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("创建socket实例失败")
        print("原因为： %s" % str(err))
    print("socket创建成功！")
    try:
        sock.connect((HOST, PORT))
        print("socket已经连接目标主机： %s , 连接的主机端口号为： %s " % (HOST, PORT))
    except socket.error as err:
        print("socket连接失败，原因为： %s" % str(err))
    while True:
        # message = ['手机盒', '0', 'ok']
        # message_dict = {'result': message}
        # for s in message:
        #     msg2Str = ",".join(message)
        start = time.time()
        end = time.time()
        it = time.strftime("%Y%m%d%H%M%S", time.localtime(start))
        print(it)
        message_dict = {'start': start, 'end': end, 'result': 'ok', 'model': 'x3d', 'object': 'phone_box', 'id': 1}
        time.sleep(1)
        # 序列化数据
        data_bytes = json.dumps(message_dict).encode()
        # 计算数据长度
        data_len = len(data_bytes)
        # 先传输数据长度，数据长度通过struct打包成4个字节的固定长度
        sock.sendall(struct.pack('i', data_len))
        # 再传输数据
        sock.sendall(data_bytes)
        print("数据已经传输，内容为：{}".format(message_dict))

    sock.close()


if __name__ == '__main__':
    msg = client()
    # print(msg)
    print("client正在运行....")
