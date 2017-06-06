
#服务器运行入口

import aps_server,zmq_version
import multiprocessing
def run():
    p1 = multiprocessing.Process(target=zmq_version.main)  # 运行web 接口，与客户端进行交互
    p2 = multiprocessing.Process(target=aps_server.main) #运行服务端的逻辑
    p1.start()
    p2.start()

if __name__ == '__main__':
    run()