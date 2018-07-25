import pickle
import time
import datetime
import difflib
import random
import pymysql.cursors

class robot(object):
    def __init__(self,msg_text,fromUser):
        # self.random=-1 #随机数
        self.user_text=msg_text#获取用户传入的信息
        self.user_name=fromUser#获取用户微信唯一id
        self.msg_text=''#返回信息


    def check(self):#check if learning moder or chat ,check only enable when chatting
        SQL = Robot_sql()
        self.msg_text=SQL.select_mysql(self.user_text)#从数据库中查询
        if self.msg_text:#非空
            return self.msg_text[self.user_text][random.randint(0, len(list(self.msg_text[self.user_text]))-1)]
        elif self.find_similar():
            print(self.msg_text)
            return self.msg_text
        else:
            return '我还没有学习这个'

    def find_similar(self):
        SQL=Robot_sql()
        find_all=SQL.select_mysql() #查询所有数据
        print("查询get")

        self.similar = 0
        self.key_all_key = list(find_all.keys()) #获取所有key 并list
        self.length = 0
        self.similar_data = []

        # print(self.key_all_key)
        for self.i in range(0, len(self.key_all_key)):
            self.similar = difflib.SequenceMatcher(None, self.user_text, str(self.key_all_key[self.i])).quick_ratio()
            if self.similar >= 0.75: #相似度大于0.75
                print(self.key_all_key[self.i])
                self.similar_data.append(self.key_all_key[self.i]) #加入待选列表
        self.length = len(self.similar_data)
        if self.length > 0:#待选列表非空
            print('length='+str(self.length))
            print('非空')
            random_data = random.randint(0, self.length - 1) #随机取值

            value=random.randint(0,len(find_all[self.similar_data[random_data]])-1)
            self.msg_text=find_all[self.similar_data[random_data]][value]

            # self.msg_text='我收到了哦，模糊查询'
            print(self.msg_text)
            print('返回true')
            return True
        else:
            print('false')
            return False

class Robot_sql():
    def __init__(self):
        self.select_words={}
    def connect_mysql(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='********',#这里输入mysql用户名
                                          password='*******',#这里输入mysql密码
                                          db='*******',#这里输入mysql库名
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def select_mysql(self,question=None):
        self.connect_mysql()
        try:
            with self.connection.cursor() as cursor:
                # Read a single record if question==None:
                if question == None:
                    sql = "SELECT `Question`, `Answer` FROM `information`"
                else:
                    sql = "SELECT `Question`, `Answer` FROM `information` WHERE Question = %s"
                cursor.execute(sql,question)
                result = cursor.fetchall()
                print('I have '+str(len(result))+' words')
                for i in range(0, len(result)):
                    temp_dict = result[i]
                    dict_key = temp_dict['Question']
                    dict_value = temp_dict['Answer']
                    self.select_words.setdefault(dict_key,[]).append(dict_value)
                # print(self.select_words)

        finally:
            self.connection.close()
            return self.select_words #返回查询到的该问题的所有记录

    def save_myself(self,more_words):
        self.connect_mysql()
        try:
            with self.connection.cursor() as cursor:
                for key in more_words:
                    # Create a new record
                    sql = "INSERT INTO `information` (`Question`, `Answer`) VALUES (%s, %s)"
                    val = more_words[key]
                    cursor.execute(sql, (str(key), val))
                    self.connection.commit()
        finally:
            self.connection.close()

