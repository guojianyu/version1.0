
import zmq
import setting
context = zmq.Context()
socket_server = context.socket(zmq.REQ)
socket_server.connect('tcp://localhost:' + setting.SERVER_PORT)
poll = zmq.Poller()
poll.register(socket_server, zmq.POLLIN)


def send(socket_server, msg):
    socket_server.send_json(msg)
    while True:  # 服务器中断会一直尝试重连
        socks = dict(poll.poll(3000))
        if socks.get(socket_server) == zmq.POLLIN:
            break
        else:
            socket_server.setsockopt(zmq.LINGER, 0)
            socket_server.close()
            poll.unregister(socket_server)
            context = zmq.Context()
            socket_server = context.socket(zmq.REQ)
            socket_server.connect('tcp://localhost:' + setting.SERVER_PORT)
            poll.register(socket_server, zmq.POLLIN)
            socket_server.send_json(msg)

send(socket_server,{'gg':1})
data = socket_server.recv_json()
print (data)