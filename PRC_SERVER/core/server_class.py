#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#python 
#2017/7/3    21:48
#__author__='Administrator'
import pika,os

class RabbitMQ_PRC(object):
    def __init__(self,myaddr):
        self.queues=myaddr#用本机IP做队列名
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))#生成消息对队
        self.channel = self.connection.channel()#生成管道
        self.channel.queue_declare(queue=self.queues)#消息收接队列

    def str_run(self,body):#处理 run的函数
        msg = os.popen(body.decode()).read()#执行系统命令
        if not msg:
            msg = '系统命令不存在'
        return msg

    def on_request(self,ch, method, props, body):#回调函数
        resp=self.str_run(body)
        print('执行完成')
        #print(resp)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,#收消息的队列
                         properties=pika.BasicProperties(correlation_id =props.correlation_id),#返回消息的队列
                         body=str(resp))#返回结果数据
        ch.basic_ack(delivery_tag = method.delivery_tag)##确保消息被 客户端接收

    def run_(self):
        self.channel.basic_qos(prefetch_count=1)#同时只处理一个消息
        self.channel.basic_consume(self.on_request, queue=self.queues)#接收消息，自动调用回调函数

        print("开始接收数据！")
        self.channel.start_consuming()#开始接收


