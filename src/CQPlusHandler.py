# -*- coding:utf-8 -*-

import cqplus
import requests
import random


class MainHandler(cqplus.CQPlusHandler):
    def handle_event(self, event, params):
        if event == 'on_private_msg':
            self.OnEvent_PrivateMsg(params)
        elif event == 'on_group_msg':
            self.OnEvent_GroupMsg(params)

    def OnEvent_PrivateMsg(self, params):
        msg = params['msg']
        self.api.send_private_msg(params['from_qq'], msg)

    def OnEvent_GroupMsg(self, params):
        self.logging.info(params['from_group'])
        if params['from_group'] in [642540069, 790583076]:
            result = self.shuangfei(params['msg'])
            if result != '':
                self.api.send_group_msg(params['from_group'], result)

    def shuangfei(self, clue):
        url = r'http://localhost:8080/api/shuangfei?clue=' + clue
        r = requests.get(url)
        if r.json()['code'] == '0000':
            return r.json()['data'][random.randint(0, 20)]
        else:
            return ''