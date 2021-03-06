# -*- coding: utf-8 -*-

import HttpServer
from KakaoBotOutput import *


class KakaoBotResponse:
    def __init__(self):
        self.outputs = []
        self.quickReplies = []
        return

    def AddText(self, text:str):
        self.AddOutput(KakaoBotTextOutput(text))
        return

    def AddImage(self, url:str, alt:str = None):
        self.AddOutput(KakaoBotImageOutput(url, alt))
        return

    def AddOutput(self, output:KakaoBotOutput):
        self.outputs.append(output)
        return

    def AddQuickReply(self, button:[KakaoBotMsgButton, KakaoBotBlockButton]):
        self.quickReplies.append(button)
        return

    def GetData(self):
        listOutputs = []
        for o in self.outputs:
            listOutputs.append({
                o.GetName(): o.GetData()
            })

        data = {
            'version': '2.0',
            'template': {
                'outputs': listOutputs,
                'quickReplies': [q.GetData() for q in self.quickReplies]
            }
        }

        return data


class KakaoBotHandler(HttpServer.HttpServerHandler):
    name = 'KakaoBotServer'

    def MakeResponse(self):
        dictJson = self.GetRequestJson()
        print('[Response] intent : %s' % dictJson['intent'])

        response = KakaoBotResponse()
        if dictJson['intent']['name'] == '폴백 블록':
            self.OnFallback(response)
            return response.GetData()

        return self.MakeSimpleResponse()

    def MakeSimpleResponse(self):
        dictRes = {}
        dictRes['version'] = '1.0'
        dictRes['data'] = {
            'msg': self.GetRequestJson()
        }
        return dictRes

    def OnFallBack(self):
        raise NotImplementedError('Fallback block method is not implmented.')

    def OnFallBackTest(self):

        if False:
            carousel = KakaoBotCarousel()

            for i in reversed(range(2)):
                card = KakaoBotBasicCard(
                    thumbnail = 'http://t1.daumcdn.net/friends/prod/editor/dc8b3d02-a15a-4afa-a88b-989cf2a50476.jpg'
                )
                card.AddButton(KakaoBotMsgButton('%d' % (i + 1), '하이'))
                card.AddButton(KakaoBotBlockButton('Block', 'TestBlock', 'Test'))
                carousel.AddOutput(card)

            carousel.SetHeader(thumbnail = 'http://t1.daumcdn.net/friends/prod/editor/dc8b3d02-a15a-4afa-a88b-989cf2a50476.jpg')
            response.AddOutput(carousel)
            response.AddOutput(carousel)
            response.AddOutput(carousel)
            response.AddOutput(carousel)
        else:
            card = KakaoBotBasicCard(
                thumbnail = 'http://t1.daumcdn.net/friends/prod/editor/dc8b3d02-a15a-4afa-a88b-989cf2a50476.jpg'
            )
            card.AddButton(KakaoBotLinkButton('나무위키', 'https://namu.wiki'))
            card.AddButton(KakaoBotBlockButton('Block', 'TestBlock', '600c5269e0c5156fec2f9406'))

            response.AddOutput(card)

            for i in reversed(range(30)):
                response.AddQuickReply(KakaoBotBlockButton(i, 'TestBlock', '600c5269e0c5156fec2f9406'))
        return

