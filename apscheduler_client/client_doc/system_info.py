import platform
import psutil
import os
import json
#platform.uname()
#uname_result(system='Darwin', node='cnadmindeiMac.local',
# release='16.3.0', version='Darwin Kernel Version 16.3.0: Thu Nov 17 20:23:58 PST 2016;
# root:xnu-3789.31.2~1/RELEASE_X86_64', machine='x86_64', processor='i386')
#machine 处理器类型
#processor  处理器的具体型号
def system_info():
    system =  platform.uname()
    mem = psutil.virtual_memory()#查看系统内存
    swap = psutil.swap_memory()
    disk = psutil.disk_partitions() #利用psutil模块的disk_partitions()方法
    partition = psutil.disk_usage('/')
    sdiskio = psutil.disk_io_counters()
    ret1 = []
    for i in disk:#分区
        ret1.append({'device':i.device.replace('/','|'),'fstype':i.fstype,' opts':i. opts})


    ret = []#获得该目录下的进程对象链表
    for i in psutil.pids():#正在运行的所有进程
        p = psutil.Process(i)
        try:
            if p.cwd() == os.getcwd():#得到在当前目录工作的进程
                cen = p.memory_info()
                pro = {"uid":i,'create_time':p.create_time(),'memory_info':{'rss':cen.rss,'vms':cen.vms,'pfaults':cen.pfaults,'pageins':cen.pageins},
                       'status':p.status(),'cwd':p.cwd().replace('/','|'),'exe':p.exe().replace('/','|'),'memory_percent':p.memory_percent()}
                ret.append(pro)
        except Exception:
            pass


    sysinfo = {
    'system': {'system': system.system,'node':system.node,'release':system.release,'machine':system.machine,'processor':system.processor},
        'memory': {'mem':{'total':mem.total,'available':mem.available,'percent':mem.percent
                                                   ,'used':mem.used,'free':mem.free,'active':mem.active,'inactive':mem.inactive,
                                                   'wired':mem.wired
                                                   },
                          'swap': {'total':swap.total,'used':swap.used,'free':swap.free,'percent':swap.percent,
                                                      'sin':swap.sin,'sout':swap.sout,
                                                    }

                          },



               'disk': {'sdiskpart':ret1,
                        'sdiskusage': {'total':partition.total,'used':partition.used,'free':partition.free,
                                       'percent':partition.percent
                                       },
                        'sdiskio': {

                                    "read_count":sdiskio.read_count,'write_count':sdiskio.write_count,
                                    'read_bytes':sdiskio.read_bytes,'write_bytes':sdiskio.write_bytes,
                                    'read_time':sdiskio.read_time,'write_time':sdiskio.write_time,

                                    }},
               'proinfo': ret
               }

    return sysinfo

#print (sysinfo)#客户端上传服务器的设备信息
"""
#内存信息
mem = psutil.virtual_memory()#查看系统内存
swap = psutil.swap_memory()
print (mem)
print (mem.total)#系统总计内存
print (mem.used)#系统使用内存
print (mem.free)#系统空闲内存
print(psutil.swap_memory())#获取swap内存信息


"""
#查看全部进程

#print (psutil.pids())#全部进程号
"""
ret = []
for i in psutil.pids():#正在运行的所有进程
    p = psutil.Process(i)
    try:
        if p.cwd() == os.getcwd():#得到在当前目录工作的进程
            ret.append(p)
            print (i)#进程号
            print (p)
            print (p.create_time())  # 进程创建时间
            print (p.memory_info())#进程内存rss,vms 信息
            print (p.name())
            print (p.status())#进程状态
            print (p.exe())#进程bin路径
            print (p.cwd())#进程的工作目录绝对路径
            print (p.memory_percent())#进程内存利用率
    except Exception:
        pass
"""

"""
#获取磁盘信息
disk = psutil.disk_partitions() #利用psutil模块的disk_partitions()方法
print (disk)#获取分区的使用情况

partition = psutil.disk_usage('/')
print (partition)#获取磁盘的总io个数，读写信息

sdiskio = psutil.disk_io_counters()
print(sdiskio)#磁盘IO信息包括read_count(读IO数)，write_count(写IO数)
#read_bytes(IO写字节数)，read_time(磁盘读时间)，write_time(磁盘写时间)
"""
#memory 和disk中的元素格式为sdiskio(read_count=193062, write_count=63902, read_bytes=6184709632, write_bytes=4964189696, read_time=2155503, write_time=1626281)
#取值为sysinfo['disk']['sdiskio'].read_count
#sysinfo['disk']['sdiskpart']的值是一个链表，它包含多个磁盘的磁盘情况
#system 是操作系统信息名称  ，memmory是内存的详细信息，mem是物理内存的信息，swap是虚拟内存的具体信息 disk是磁盘信息

#进程信息是一个链表，链表的每一个元素为字典
