#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#python 
#2017/7/3    22:01
#__author__='Administrator'
import os ,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#获取相对路径转为绝对路径赋于变量
sys.path.append(BASE_DIR)#增加环境变量

from core.client_class import Threa

if __name__ == '__main__':
    RPCS=Threa()
    response=RPCS.th_start()
        #RPCS.call(str_l)
        #print(response)