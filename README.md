# Python-ChatRoom
一个简单的聊天室

## Usage

1. 首先启动服务端 

```python
python3 server.py 127.0.0.1 port 
```

2. 启动客户端

```python
python3 client.py [server_host] [server_port] [client_host] [client_port]
```
例如
```python
python client.py 127.0.0.1 2223 127.0.0.1 2222
```


3. 设置username和password

```
username: mki
password: mki
```

4. 选择chat mode

```
b:(broadcast)       群聊 所有用户可见
s:(solo)            私聊 仅选择用户可见
l:(list all users)  显示所有在线用户
e:(exit)            退出chatroom
```

