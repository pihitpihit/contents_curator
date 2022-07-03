# -*- coding: utf-8 -*-

from KakaoBotHandler import KakaoBotHandler
from KakaoBotHandler import KakaoBotResponse
from KakaoBotOutput import *

class ContentsCuratorHandler(KakaoBotHandler):

    def OnFallback(self, response):

        testData = [
            'aaa.txt',
            'bbb.png',
            'ccc.mp3',
        ]

        self.BrowserCard(response, testData)

        return

    def BrowserCard(self, response, entryList):
        thumbnail='http://t1.daumcdn.net/friends/prod/editor/dc8b3d02-a15a-4afa-a88b-989cf2a50476.jpg'
        if False:
            data = ''
            for i in range(len(entryList)):
                data += '[%d] %s\n' %(i, entryList[i])
                response.AddQuickReply(KakaoBotMsgButton(str(i), str(i)))

            card = KakaoBotBasicCard(thumbnail=thumbnail, title='AAA', desc=data)
            response.AddOutput(card)

        itemCard = KakaoBotItemCard()
        for i in range(len(entryList)):
            itemCard.AddItem(str(i), entryList[i])
        itemCard.SetItemListAlignment('left')
        itemCard.SetItemListSummary('SUMMARY', 'DESCRIPTION')

        if False:
            itemCard.SetHead('head')
        else:
            itemCard.SetProfile('PROFILE', 'https://t1.kakaocdn.net/openbuilder/docs_image/aaairline.jpg')

        itemCard.SetTitle('TITLE')
        itemCard.SetDesc('DESCRIPTION')

        itemCard.SetThumbnail(thumbnail, 800, 400)
        itemCard.SetImageTitle('image title', 'image desc')

        itemCard.AddButton(KakaoBotMsgButton('<', '<'))
        itemCard.AddButton(KakaoBotMsgButton('>', '>'))
        itemCard.SetButtonLayout('horizontal')

        response.AddOutput(itemCard)
        return

