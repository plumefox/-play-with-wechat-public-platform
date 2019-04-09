# -play-with-wechat-public-platform
微信公众号,微信推送,微信回复,wechat,微信

# 项目简述：
该项目是一个基于python实现的微信公众号上课程推送的程序。  
该项目兼有微信公众号机器人，并且可以对关注用户进行课程推送。  
注：目前课程推送功能所使用的数据库为sqlserver  

## 如何使用
### 公众号机器人功能  
1. 下载完成以后，打开robot.py，修改其中的数据库和密码，并完成数据库的建立（注意 使用mmsql数据库）  
数据表名为 information  
字段名为 Question ， Answer  

2.

### 课程推送功能
1. 下载完成以后，打开SqlServerConnect.py，修改其中的数据库和密码，并完成数据库的建立  
2. 根据需要修改 课程推送.py 文件内的内容  


## 目录结构
main.py 文件是入口
receive.py 公众号收到消息后的解析操作
reply.py 公众号回复消息的包装操作
handle.py 主要文件

get函数用来验证
post函数正常接收
