import SqlServerConnect
import json
import requests

url="https://api.weixin.qq.com/cgi-bin/message/template/send?access_token="
header={"Content-type":"appliacation/json"}
def set_Todays_Class(StuID,StuName,ClassName,ClassTime,CLassroom,OpenID="yourWechatOpenID"):
    dict = ({
        'touser': OpenID,
        "template_id": "your template_id",
        "url": "your url",
        "topcolor": "#FF0000",
        ""
        'data': {
            'first': {
                'value': StuID+" "+StuName+'推送标题',
                "color": "#173177"
            },
            'keyword1': {
                'value': ClassName,
                "color": "#173177"
            },
            'keyword2': {
                'value':ClassTime,
                "color": "#173177"
            },
            'keyword3': {
                'value': CLassroom,
                "color": "#173177"
            },
            'remark': {
                'value': None,
                "color": "#173177"
            },
        }

    })
    # dict_after['touser']=OpenID
    # dict_after['data'['keyword1'['value']]]=ClassName
    return dict
def send_to_user(result):
    for key in result:
        class_count = len(result[key])
        for i in range(class_count):
            information = set_Todays_Class(result[key][i][0],result[key][i][1],result[key][i][2], str(result[key][i][3]) + "-" + str(result[key][i][4]),
                                  result[key][i][5]) #StuID,StuName,ClassName,ClassRoom,OpenID
            print(information)
            jsonx = json.dumps(information)

            access_token = get_token()
            response = requests.post(url + access_token, data=jsonx)
            print(response.text)

            # break
        # break

def get_token():
    #-----------------------------------------------------------
    token = "your token url"
    my = requests.get(token)
    print(my.text)
    data  = json.loads(my.text)
    access_token = data['access_token']
    #--------------------------------------------------------------
    # access_token = "token"
    return access_token
    #--------------------------------------------------------------
    # response = requests.post(url+access_token, data = jsonx)

if __name__=='__main__':
    s=SqlServerConnect.Connect()
    result=s.EveryDay_Class("20180510")
    send_to_user(result)
