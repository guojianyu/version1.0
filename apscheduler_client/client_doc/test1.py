
import zmq
import setting
context = zmq.Context()
socket_server = context.socket(zmq.REQ)
socket_server.connect('tcp://localhost:' + '55555')
poll = zmq.Poller()
poll.register(socket_server, zmq.POLLIN)


def send(socket_server, msg):
    return socket_server.send_json(msg)

a = send(socket_server,{'gg':1})
print (a,'s')
data = socket_server.recv_json()
print (data,'r')