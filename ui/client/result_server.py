import json
import random
import socket
import struct
import time

# from demo.resource import read_yml as read


names = ["lesional_tissue_1", "lesional_tissue_2", "lesional_tissue_3", "lesional_tissue_4"]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('创建socket成功')
ip_port = ('127.0.0.1', 8888)
# 绑定一个端口
sock.bind(ip_port)
# 监听一个端口,这里的数字3是一个常量，表示阻塞3个连接，也就是最大等待数为3
sock.listen(100)
# 接受客户端的数据，并返回两个参数，a为连接信息，b为客户端的ip地址与端口号
a, b = sock.accept()
print("连接到主机： %s" % str(b))
detect_id = [1] * 4
while True:
    # message = ['手机盒', '0', 'ok']
    # message_dict = {'result': message}
    # for s in message:
    #     msg2Str = ",".join(message)
    start = time.time()
    end = time.time()
    it = time.strftime("%Y%m%d%H%M%S", time.localtime(start))
    num = random.randint(0, 3)
    message_dict = {'start': start, 'end': end, 'result': (random.random(), random.random()), 'model': 'x3d', 'object': names[num], 'id': detect_id[num]}
    detect_id[num] += 1
    time.sleep(1)
    # 序列化数据
    data_bytes = json.dumps(message_dict).encode()
    # 计算数据长度
    data_len = len(data_bytes)
    # 先传输数据长度，数据长度通过struct打包成4个字节的固定长度
    a.sendall(struct.pack('i', data_len))
    # 再传输数据
    a.sendall(data_bytes)
    print("数据已经传输，内容为：{}".format(message_dict))

sock.close()
