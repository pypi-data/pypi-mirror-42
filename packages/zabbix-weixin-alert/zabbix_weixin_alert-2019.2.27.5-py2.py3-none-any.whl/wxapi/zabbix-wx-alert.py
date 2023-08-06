#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
 @Author: 郝天飞/Talen Hao (talenhao@gmail.com)
 @Site: talenhao.github.io
 @Since: 2/26/19 4:37 PM
"""

import wxapi
import json
import sys

name = "zabbix-wx-alert"

if __name__ == '__main__':
    corp_id = '{}'.format(sys.argv[4])
    corp_secret = '{}'.format(sys.argv[5])
    wx = wxapi.QYWX(corp_id=corp_id, corp_secret=corp_secret)
    access_token = wx.get_access_token()

    message = {
        "touser": "@all",
        "msgtype": "text",
        "agentid": 1000002,
        "safe": 0,
        "text":
            {
                "content": ""
            }
    }
    message["agentid"] = sys.argv[6]
    message["text"]["content"] = "\n_____ \n".join(sys.argv[1:4])
    message = json.dumps(message)
    print(message)
    send_message = wx.send_message(access_token_value=access_token, message=message)
    print(send_message.json())
