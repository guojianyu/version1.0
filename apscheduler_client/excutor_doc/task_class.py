#-*- utf-8 -*-
from excutor_doc.jd_tools import * #
import os

class jd_task_class:#执行器和解析器的入口类，找到对应的执行器和解析器
    def get_urls(self,task):#得到url

        topic = task['topic']
        #curdir = os.getcwd()
        curdir = os.path.abspath(os.path.dirname(__file__))
        script_path = os.path.join(curdir, topic + '.py')
        if jd_tools.file_is_exist(script_path):
            exec("from excutor_doc.%s import *"%(topic))
            load_class = eval(topic)
            return load_class.get_urls(task)
        else:
            return

    def parser(self,html,task):
        topic = task['topic']
        curdir = os.getcwd()
        script_path = curdir + '/' + topic + '.py'
        if jd_tools.file_is_exist(script_path):
            exec("from %s import *" % (topic))
            load_class = eval(topic)
            return load_class.parser(html,task)
        else:
            return

