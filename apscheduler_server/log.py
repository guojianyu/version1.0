import logging

class log:
    def __init__(self):

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='record.log',
                            filemode='a')
        #################################################################################################
        # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        #################################################################################################

    def write_log(self, arg):  # 写日志 arg的格式 {'level':,'content':....}level是写扫描类型的日志，content是日志内容
        level = arg['level']  # 得到日志等级
        content = arg['content']  # 日志内容
        if level == 'info':
            logging.info(content)
        elif level == 'debug':
            logging.debug(content)
        elif level == 'warning':
            logging.warning(content)
        elif level == 'error':
            logging.error(content)

if __name__ =='__main__':
    arg = {'level':'info','content':'test'}
    obj = log()
    obj.write_log(arg)

