#!/usr/local/bin/python3
# -*- coding:UTF-8 -*-
# AUTHOR: Mki
# FILE: ~/Desktop/DailyCode/Python/加强版涩图聊天室/client.py
# DATE: 2019/11/12 周二
# TIME: 14:31:12

# DESCRIPTION: 网络编程课作业  聊天室客户端
import threading
from socket import socket, AF_INET, SOCK_DGRAM
import json
import os
import sys

class Client():
    def __init__(self,addr):
        '''
        初始化
        '''
        self.addr = addr
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(addr)
        self.auth = {}
        self.queue = []
        self.start()

    def login(self):
        '''
        用户登陆
        '''
        name = str(input("username: "))
        pwd = str(input("password: "))
        self.auth = {
            "name": name,
            "pwd": pwd
        }

        msg = {}
        msg["auth"] = self.auth
        msg["type"] = "notice"
        msg = json.dumps(msg)
        msg = bytes(msg, encoding='utf-8')
        self.sock.sendto(msg, ('localhost',20000))

    def recieve(self,addr):
        '''
        接收消息
        '''
        while True:
            msg, addr = self.sock.recvfrom(8192)
            msg = str(msg,encoding="utf-8")
            self.queue.append(msg)
            self.chatWindow()

    def chatWindow(self):
        '''
        聊天界面
        '''
        os.system('clear')
        print("################# Mki's ChatRoom #################")
        if len(self.queue)>=6:
            for msg in self.queue[-6:]:
                print(f'{msg} \n')
        else:
            for msg in self.queue:
                print(f'{msg} \n')
        print("################# Mki's ChatRoom ################")
        print("mode b:(broadcast) s:(solo) l:(list all users)")


    def pack(self):
        '''
        消息处理
        '''
        msg = {}
        msg["auth"] = self.auth
        mode = input("mode b:(broadcast) s:(solo) l:(list all users)\n")
        if mode == "s":
            msg["type"] = "solo"
            msg["toWho"] = str(input("to: "))
            msg["text"] = str(input(": "))
        elif mode == "b":
            msg["type"] = "broadcast"
            msg["text"] = str(input(":"))
        elif mode == "l":
            msg["type"] = "show"
        elif mode == "e":
            sys.exit()
        else:
            msg["type"] = ""
            print("Wrong order, please input b:(broadcast) s:(solo) l:(list all users)")
        msg = json.dumps(msg)
        msg = bytes(msg, encoding='utf-8')
        return msg
  

    def start(self):
        t = threading.Thread(target=self.recieve,args=(self.addr,))
        t.setDaemon(True)
        t.start()

        self.login()
        while True:
            msg = self.pack()
            self.sock.sendto(msg, ('localhost',20000))


if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]
    print(f"Target:{host} {port}")
    Client((host,int(port)))



