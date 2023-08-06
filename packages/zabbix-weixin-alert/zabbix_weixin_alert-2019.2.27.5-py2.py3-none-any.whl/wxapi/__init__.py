# -*- coding: UTF-8 -*-

"""
 @Author: 郝天飞/Talen Hao (talenhao@gmail.com)
 @Site: talenhao.github.io
 @Since: 2/26/19 3:43 PM
"""

name = "zabbix-weixin-alert"

import json
import requests


class QYWX(object):
    def __init__(self, corp_id=None, corp_secret=None, api_url='https://qyapi.weixin.qq.com/cgi-bin/'):
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.api_url = api_url

    def get_access_token(self):
        access_token_params = {}
        access_token_params['corpid'] = self.corp_id
        access_token_params['corpsecret'] = self.corp_secret
        access_token_url = "gettoken"
        access_token = requests.get(url=self.api_url + access_token_url, params=access_token_params)
        access_token_value = access_token.json()["access_token"]
        return access_token_value

    def send_message(self, access_token_value=None, message=None):
        message_url = "message/send"
        url = "{}{}?access_token={}".format(self.api_url, message_url, access_token_value)
        send_post = requests.post(url=url, data=message)
        return send_post
