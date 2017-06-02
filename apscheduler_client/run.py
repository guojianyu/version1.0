#客户端的整体逻辑入口

from client_doc import aps_client,recv_interface
from center_layer import center_layer
from excutor_process import scan_process
import multiprocessing


def run():


    p3 = multiprocessing.Process(target=center_layer.main)  # 运行中间层
    p1 = multiprocessing.Process(target=aps_client.main)#运行客户端
    p2 = multiprocessing.Process(target=recv_interface.run)#运行客户端对外接口
    p0 = multiprocessing.Process(target=scan_process.process_main)


    p1.start()
    p2.start()


    p3.start()
    p0.start()



if  __name__ == '__main__':
    run()