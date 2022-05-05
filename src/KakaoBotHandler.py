# -*- coding: utf-8 -*-

import HttpServer

class KakaoBotHandler(HttpServer.HttpServerHandler):
    name = 'KakaoBotServer'

    def Response(self):
        return self.GetRequestJson()['userRequest']['utterance']
