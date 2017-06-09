class create_uploadtask:
    def __init__(self):
        pass

    def create_task(self,task):#将解析得到的数据拼接为发送任务
        #不发送ip,通过device_id服务器可以得到。
        guid = task['guid']
        crawl_time = task['crawl_time']
        version= task['version']
        device_id = task['device_id']
        data = task['data']
        bulk = task['bulk']
        upload_task = {

            'upload_time': '', 'client_info': {'device_id': device_id, 'other': ''},
            # 'upload_time'上传时间,客户端上传数据时填充，'client_info'客户端信息
            'format': {'compress': 0, 'encryption': 0},  # compress压缩，encryption加密，0代表no，1代表yes
            'content': {'data_count': '', 'crawl_time': crawl_time, 'data': []},
            # 上传的数据相关，'data_count'数据个数，'crawl_time'爬取时间，data:具体的数据
            'save_info': {'version': version, 'bulk': bulk},  # 保存信息相关，'version',保存器版本号，'bulk':0零散的数据，需要拼接。1：完整的数据直接入库
            'guid': guid,  # 数据所属任务总任务id
            'upload_flag': 0  # 上传成功与否标识位，0没有上传，1上传成功

        }
        if not bulk:#bulkd注明要进行拆分，数据传递进去，返回一个拆分数据的列表
            data_list = self.explain(data)
            for item in data_list:
                #将数据填充到upload中的content.data,content.data_count = len(item),将一个大任务，分解为小任务，多次发送
                #发送upload_task
                pass

    def explain(self,data):#如果发送数据太大或者有拆分数据的需求支持将任务进行拆分存储发送
        #负责将发送数据拆分，压缩，加密。
        data_list = []
        #拆分逻辑
        return  data_list

        pass
