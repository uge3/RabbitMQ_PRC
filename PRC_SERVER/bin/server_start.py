#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#python 
#2017/7/3    21:47
#__author__='Administrator'
import os ,sys
import socket
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#获取相对路径转为绝对路径赋于变量
sys.path.append(BASE_DIR)#增加环境变量
from core.server_class import RabbitMQ_PRC
if __name__=='__main__':

    #获取本机电脑名
    myname = socket.getfqdn(socket.gethostname())
    #获取本机ip
    myaddr = socket.gethostbyname(myname)
    print (myname)
    print (myaddr)
    ipList = socket.gethostbyname_ex(socket.gethostname())
    print(ipList[2][1])
    myaddr=ipList[2][1]
    pers=RabbitMQ_PRC(str(myaddr))
    pers.run_()