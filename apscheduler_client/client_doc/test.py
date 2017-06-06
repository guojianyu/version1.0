import zmq
import setting
context = zmq.Context()
socket_client = context.socket(zmq.REP)
socket_client.bind("tcp://*:" + setting.SERVER_PORT)
data = socket_client.recv_json()
print (data)
socket_client.send_json(['hhh',])
