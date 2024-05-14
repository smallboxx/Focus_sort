import socket


def createSocket(host, port, listen_num):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as err:
        print("创建socket实例失败")
        print("原因为： %s" % str(err))
    print("socket创建成功！")
    try:
        sock.bind((host, int(port)))
    except socket.error as err:
        print("socket绑定端口失败，原因为： %s" % str(err))
    # 设置监听端口的最大连接数
    print("socket绑定成功！")
    sock.listen(listen_num)
    sock.setblocking(0)
    print("socket监听....")
    return sock
