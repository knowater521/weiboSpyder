from web.Controller.function.weiboApi import Client
from web import app
import jieba
import re

# My app key
# APP_KEY='2234918214'
# APP_SECRET='8e7c9832fd113ad36bed58ff8892a098'
# CALLBACK_URL='https://api.weibo.com/oauth2/default.html'

# Weico App Key
APP_KEY = '211160679'
APP_SECRET = '63b64d531b98c2dbff2443816f274dd3'
CALLBACK_URL = 'http://oauth.weico.cc'
AUTH_URL = 'https://api.weibo.com/oauth2/authorize'

baseurl = ''


def main():
    c = Client(APP_KEY, APP_SECRET, CALLBACK_URL)
    # return
    print(c.token)


    # mytoken ={'uid':'1768227640','access_token':'2.00emSfvB06XASO115dbe63f2_y5mtC','expires_at':4616404470,
    #           'remind_in':'3153599999'}
    # c=Client(APP_KEY, APP_SECRET, CALLBACK_URL, mytoken)
    # print(c.authorize_url)
    # token = 'd531c84d32c85686f1af428e987a3168'
    # c.set_code(token)
    # print(c.token)

    # print('Login success')
    # public_loc=c.get('friendships/friends/bilateral',uid=1768227640)
    # print(public_loc)

    # public_weibo=c.get('statuses/public_timeline',count=50)  # 获取用户UID
    # print("收集到{}条".format(public_weibo['total_number']))
    # lists = public_weibo["statuses"]
    # punctuation='[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]'
    # for one in lists:
    #     nickname = one['user']['name']
    #     location = one['user']['location']
    #     content = one['text']
    #     clear_content =re.sub(r"\[(.+?)\] | @(.+?) |(HTTP|http)s?://[^,， ]+","",content)
    #     clear_content = re.sub(punctuation,"",clear_content)
    #     seg_list=jieba.cut(clear_content)
    #     print('昵称:{} 位置:{} \n 内容:{}\n关键词:{}\n\n'.format(nickname,location,content," ".join(seg_list)))
if __name__=='__main__':
    main()
