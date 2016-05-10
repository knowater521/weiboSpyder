from web.Controller.function.weiboApi import Client

# My app key
# APP_KEY='2234918214'
# APP_SECRET='8e7c9832fd113ad36bed58ff8892a098'
# CALLBACK_URL='https://api.weibo.com/oauth2/default.html'

# Weico App Key
APP_KEY = '211160679'
APP_SECRET = '63b64d531b98c2dbff2443816f274dd3'
CALLBACK_URL = 'http://oauth.weico.cc'
AUTH_URL = 'https://api.weibo.com/oauth2/authorize'

weibo = Client(APP_KEY, APP_SECRET, CALLBACK_URL)
import web.Controller.weibo_view