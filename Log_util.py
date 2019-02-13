#!/usr/bin/python
# _*_ coding:utf-8 _*_

import logging
import time
import os


#获取脚本所在的路径
#cur_path = os.path.dirname(os.path.realpath(__file__))
cur_path = os.getcwd()
#print cur_path

#设置日志路径
log_path = os.path.join(cur_path,'logs/')


#检查日志目录是否存在，如果不存在则新建一个目录
if not os.path.exists(log_path):
    os.mkdir(log_path)

#定义当前时间
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))

class Logger:
    def __init__(self):

        #设置日志文件名称
        self.logname = log_path+rq+'.log'

        #设置日志文件格式
        self.formatter = logging.Formatter('[%(asctime)s]-[%(name)s]-%(levelname)s: %(message)s')

        #创建一个Handler，用于写入日志文件
        self.fh = logging.FileHandler(self.logname)
        #设置日志等级开关
        self.fh.setLevel(logging.DEBUG)
        #定义Handler的输出格式
        self.fh.setFormatter(self.formatter)

        #创建一个Hander,用于输出到控制台
        self.ch = logging.StreamHandler()
        # 设置日志等级开关
        self.ch.setLevel(logging.DEBUG)
        # 定义Handler的输出格式
        self.ch.setFormatter(self.formatter)

#添加日志内容到句柄并返回添加完成的句柄
    def console_log(self,appName):
        #获取一个实例，指定name，返回一个名称为name的Logger实例。如果再次使用相同的名字，是实例化一个对象。未指定name，返回Logger实例，名称是root，即根Logger。
        logger = logging.getLogger(appName)
        #给实例添加Handle
        logger.addHandler(self.fh)
        logger.addHandler(self.ch)
        logger.setLevel(logging.DEBUG)
        return logger

# log = Logger().console_log(os.path.basename(__file__))
# log.info('try try try')
# log.warning('hahaha')
# log.error('nonono')