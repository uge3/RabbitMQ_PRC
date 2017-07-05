#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#python 
#2017/7/3    21:59
#__author__='Administrator'

import pika
import uuid
import threading
import random

class FibonacciRpcClient(object):
    def __init__(self):
        self.credentials=pika.PlainCredentials("test","test")
        #self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))#生成连接的服务端 ip
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("192.168.11.51",15672,'/',self.credentials))#生成连接的服务端 ip
        self.channel = self.connection.channel()#创建一个管道

    def get_respon(self,cal_queue,cal_id):#取任务信息
        self.response=None
        self.callback_id=cal_id#队列名
        self.channel.basic_consume(self.on_response,queue=cal_queue)# 使用回调函数
        while self.response is None:
            self.connection.process_data_events()#非阻塞模式接收消息
        return self.response#返回

    def on_response(self, ch, method, props, body):#回调函数
        if self.callback_id == props.correlation_id:#判断服务端返回的队列名是否与当前所生成的队列名一致
            self.response = body#  将服务端的结果赋于返回来的结果变量
        ch.basic_ack(delivery_tag = method.delivery_tag)##确保消息被 接收

    def call(self, queues,n):#发送消息的函数
        result = self.channel.queue_declare(exclusive=False)#随机生成一个队列，收消息后不删除
        self.callback_queue = result.method.queue#赋于管道 变量
        self.corr_id = str(uuid.uuid4())#生成一个服务端返回消息的队列名
        self.channel.basic_publish(exchange='',
                                   routing_key=queues,#队列名
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,#发送的管道队列名
                                         correlation_id = self.corr_id,#发送给服务端，用于返回消息的队列名
                                         ),
                                   body=str(n))#发送的内容数据
        return self.callback_queue,self.corr_id#返回管道名 队列id号

class Threa(object):#线程 类
    def __init__(self):
        self.info={}#生成一个字典
        self.help_info='''         指令示例\033[36;1m
        run "df -h" --hosts 192.168.3.55 10.4.3.4
        --- ------- ------- ------------ --------
        运行 指令    主机    ip 1#        ip 2#
        check_task_all      #查看任务列表
        check_task  25413   #查看具体id任务信息，过后删除
        helps               #查看指令帮助
        \033[0m'''

    def check_task_all(self,cmd):#查看所有任务信息

        for i in self.info:
            print("任务id:%s,服务端:%s,命令:%s"%(i,self.info[i][0],self.info[i][1]))
    def check_task(self,take_id):#查看任务
        try:
            id=int(take_id.split()[1])#取任务ID
            #print(id,'任务ID')
            cal_queue=self.info[id][2]#管道名
            #print(cal_queue,'队列')
            cal_id=self.info[id][3]#消息队列位置
            #print(cal_id,'消息位置')
            clinets=FibonacciRpcClient()#调用类
            rest=clinets.get_respon(cal_queue,cal_id)#取任务信息
            print('任务执行结果:',rest.decode())#打印
            del self.info[id]#从字典中删除对应任务
        except Exception as e:
            print(e)
            return

    def run(self,str_l):#run函数
        addr_l=self.attr_l(str_l)#获取IP
        oreds=self.oreds_(str_l)#获取 命令
        #print(oreds,'上传命令')
        for i in addr_l:#取出IP
            tak_id=random.randint(10000,99999)#任务ID生成
            #print(tak_id,'任务ID')
            obj=FibonacciRpcClient()#生成连接类
            r=obj.call(i,oreds)#ip做队列名  命令
            self.info[tak_id]=[i,oreds,r[0],r[1]]#写入字典 tak_id{ ip 命令 管道名 队列名}
        return self.info

    def retf(self,str_l):#反射命令
        sl=str_l.split()[0]#取命令开头
        if sl=='helps':
            self.helps()
        if len(str_l.split())==1 and sl!='check_task_all' :
            return
        if hasattr(self,sl):#是否存在
            func=getattr(self,sl)#调用
            rer=func(str_l)#执行
            #print(rer)
            if rer is not None:
                for i in  rer:
                    print("任务id:%s"%i)

    def attr_l(self,n):#命令分解函数
        attr=n.split("--")##用--分割
        addr=attr[1].split()[1:]#获取IP列表
        return addr#返回IP列表

    def oreds_(self,n):#获取 命令
        oreds=n.split("\"")[1]##用"分割取命令
        return oreds#返回 命令

    def helps(self):#查看指令帮助
        print(self.help_info)

    def th_start(self):#开始
        self.helps()
        while True:
            str_l=input(">>:").strip()
            if not str_l:continue#如果为空重新输入
            t1=threading.Thread(target=self.retf,args=(str_l,))#创建新线程 调用反射函数
            t1.start()#开始线程