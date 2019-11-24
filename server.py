# -*- coding:UTF-8 -*-
# AUTHOR: Mki

# DESCRIPTION:   聊天室服务器

import time
from  socket import socket, AF_INET, SOCK_DGRAM
import logging
import json
import os
import sys

# logFormat = "%(asctime)s - %(levelname)s - %(message)s"
# logging.basicConfig(level=logging.INFO,format=logFormat,filename="test.log",filemode="a")

class Server():
    def __init__(self,address):
        '''
        初始化服务器
        '''
        self.addr = address
        self.userList = {}
        self.start()

    def start(self):
        '''
        服务器开始接收消息
        '''
        print('[*]srever start')
        self.recieve(self.addr)

    def send(self,msg,addr):
        '''
        发送消息
        '''
        s = socket(AF_INET, SOCK_DGRAM)
        s.sendto(msg, addr)

    def addUser(self,auth,addr):
        '''
        添加用户
        '''
        self.userList[auth["name"]] = {}
        self.userList[auth["name"]]["addr"] = addr
        self.userList[auth["name"]]["pwd"] = auth["pwd"]

    def auth(self,auth,addr):
        '''
        用户权限认证
        '''
        if auth["name"] not in self.userList:
            self.addUser(auth,addr)
            return True
        else:
            if auth["pwd"] == self.userList[auth["name"]]["pwd"]:
                return True
            else:
                return False
    
    def solo(self,text,addr,username=''):
        '''
        私聊消息发送    
        '''
        text = bytes(text,encoding='utf8')
        if username in self.userList:
            addr = self.userList[username]["addr"]
            print(f"secret message to {username} ")
            self.send(text,addr)
        else:
            print(f"secret message 'send failed'")
            self.send(text,addr)

    def boardcast(self,text):
        '''
        群聊消息发送
        '''
        text = bytes(text,encoding='utf8')
        for user in self.userList:
            print(f"boardcast message :{str(text)} ")
            self.send(text,self.userList[user]["addr"])

    def handle(self,msg,addr):
        '''
        消息接收处理器
        '''
        if self.auth(msg["auth"],addr):
            if msg["type"] == "broadcast":
                text = ("[*]"+msg["auth"]["name"]+" say: "+msg["text"])
                self.boardcast(text)
            elif msg["type"] == "solo":
                text = ("[!]"+msg["auth"]["name"]+" send a secret message to you\n: "+msg["text"])
                self.solo(text,addr,msg["toWho"],)
            elif msg["type"]=="notice":
                text = ("[+]"+msg["auth"]["name"]+" add the chatRoom")
                self.boardcast(text)
            elif msg["type"]=="show":
                text = '[&]all online users\n'
                for user in self.userList:
                    text = text + user + '\n'
                self.solo(text,addr)
            else:
                pass
        else:
            text = ("Login failed")
            self.solo(text,addr)


    def recieve(self,addr):
        '''
        接收消息
        '''
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(addr)
        while True:
            msg, addr = sock.recvfrom(8192)
            msg = json.loads(msg)
            self.handle(msg,addr)

if __name__ == '__main__':
    localhost = sys.argv[1]
    localport = sys.argv[2]
    localaddr = (localhost,int(localport))
    Server(localaddr)





