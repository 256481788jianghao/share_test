# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 16:20:56 2017

@author: Administrator
"""

from socket import *

class TcpClient:
    #测试，连接本机
    HOST='127.0.0.1'
    #设置侦听端口
    PORT=1122 
    BUFSIZ=1024*10
    ADDR=(HOST, PORT)
    def __init__(self):
        self.client=socket(AF_INET, SOCK_STREAM)
        self.client.connect(self.ADDR)
        
        data_cmd = 'data_len'
        data_rec_len = 0
        data_rec_json = ''
        while True:
            data_cmd=input('>')
            #if not data:
                #break
            #python3传递的是bytes，所以要编码
            self.client.send(data_cmd.encode('utf8'))
            #print('发送信息到%s：%s' %(self.HOST,data_cmd))
            if data_cmd.upper()=="QUIT":
                break            
            data=self.client.recv(self.BUFSIZ)
            if not data:
                break
            elif data.decode('utf8')[0:9] == 'DATA_LEN:':
                data_rec_len = str(data.decode('utf8')[10:-1])
                print('data_len='+data_rec_len)
                #data_cmd = 'data_send'
            elif data.decode('utf8')[0:10] == 'DATA_SEND:':
                data_rec_json += data.decode('utf8')[11:-1]
                print('data_rec_json_len='+str(len(data_rec_json)))
            elif data.decode('utf8') == 'ALL_DATA_END':
                print('data_rec_json_len='+str(len(data_rec_json)))
                break
            #print('从[server]%s收到信息：%s' %(self.HOST,data.decode('utf8')))
            
            
if __name__ == '__main__':
    client=TcpClient()