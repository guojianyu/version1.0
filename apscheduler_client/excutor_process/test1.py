

import os,importlib
topic = 'test'
curdir = os.path.abspath(os.path.dirname(__file__))
print (curdir)
script_name = ".".join(('script_doc', topic))  # 类型与脚本名称关联
m1 = importlib.import_module(script_name, curdir)  # 引入collection_doc目录下的文件.
print (m1)
obj = m1.a()  # 实例话模块的类
obj.test()  # 调用方法