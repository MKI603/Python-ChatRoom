# -*- coding:UTF-8 -*-
# AUTHOR: Mki

# DESCRIPTION:  聊天室客户端
import threading
from socket import socket, AF_INET, SOCK_DGRAM
import json
import os
import sys

class Client():
    def __init__(self,localAddr,serverAddr):
        '''
        初始化
        '''
        self.addr = localAddr
        self.serverAddr = serverAddr
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(localAddr)
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
        self.sock.sendto(msg, self.serverAddr)

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
        print("################# ChatRoom #################")
        if len(self.queue)>=6:
            for msg in self.queue[-6:]:
                print(f'{msg} \n')
        else:
            for msg in self.queue:
                print(f'{msg} \n')
        print("################# ChatRoom ################")
        print("mode b:(broadcast) s:(solo) l:(list all users)")


    def pack(self):
        '''
        消息处理
        '''
        msg = {}
        msg["auth"] = self.auth
        mode = input("mode b:(broadcast) s:(solo) l:(list all users) e:(exit)\n")
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
            print("Wrong order, please input b:(broadcast) s:(solo) l:(list all users) e:(exit")
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
            self.sock.sendto(msg, self.serverAddr)


if __name__ == "__main__":
    localHost = sys.argv[1]
    localPort = int(sys.argv[2])
    localAddr = (localHost,int(localPort))

    romoteHost = sys.argv[3]
    romotePort = sys.argv[4]
    romoteAddr = (romoteHost,int(romotePort))
    
    Client(localAddr,romoteAddr)



