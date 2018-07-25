# -*- coding: utf-8 -*-
# filename: handle.py

#这个文件用来接受微信服务器传过来的get和post请求，并对token进行加密
import hashlib
import web
import reply
import xml.etree.ElementTree as ET
# import SqlServerConnect

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "PlumeFoxRobotPlufo" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            print(list)
            list.sort()
            print(list.sort())
            list2=''.join(list)
            sha1 = hashlib.sha1()
            sha1.update(list2.encode('utf-8'))
            hashcode = sha1.hexdigest()
            print ("handle/GET func: hashcode, signature: ", hashcode,"/n", signature)
            if hashcode == signature:
                print(echostr)
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument

    def POST(self):
        try:
            str_xml = web.data()  # 获得post来的数据
            print("xml为")
            print(str_xml)
            xml = ET.fromstring(str_xml)  # 进行XML解析
            print("解析后")
            print(xml)
            print("\n")
            # print(content)
            msgType = xml.find("MsgType").text
            fromUser = xml.find("FromUserName").text
            toUser = xml.find("ToUserName").text
            print(toUser)
            print(msgType)
            if msgType == 'event':
                print("event!!!!!!!!!!!!!!\n")
                msg_event=xml.find("Event").text
                print(msg_event)
                msg_callback=self.handle_event(msg_event)
            else:
                content = xml.find("Content").text  # 获得用户所输入的内容
                #以下调用
                # SQL_reply=SqlServerConnect.Connect() #实例化
                # msg_callback=Robot_reply.check()
                msg_callback="你输入了"+content
            replyMsg = reply.TextMsg(fromUser, toUser, msg_callback)
            return replyMsg.send() #返回xml
        except Exception as Argument:
                return Argument


    def handle_event(self,msg_event):
        if msg_event=='subscribe':
            content='欢迎关注'
            return content
        elif msg_event=='unsubscribe':
            content='取关'
            return content



