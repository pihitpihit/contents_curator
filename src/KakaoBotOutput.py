# -*- coding: utf-8 -*-

from KakaoBotButton import *

class KakaoBotOutput:
    def __init__(self):
        return

    def GetName(self):
        raise NotImplementedError('KakaoBotOutput.GetName method must be called after impement by a derived class.')

    def GetData(self):
        raise NotImplementedError('KakaoBotOutput.GetData method must be called after impement by a derived class.')


class KakaoBotTextOutput(KakaoBotOutput):
    def __init__(self, text:str):
        self.text = text
        return

    def GetName(self):
        return 'simpleText'

    def GetData(self):
        return {
            'text': self.text
        }


class KakaoBotImageOutput(KakaoBotOutput):
    def __init__(self, url:str, alt:str = None):
        self.url = url
        self.alt = alt
        if self.alt is None:
            self.alt = 'InvalidImageUrl'
        return

    def GetName(self):
        return 'simpleImage'

    def GetData(self):
        return {
            'imageUrl': self.url,
            'altText': self.alt
        }


class KakaoBotCard(KakaoBotOutput):
    def __init__(self):
        KakaoBotOutput.__init__(self)
        return


class KakaoBotBasicCard(KakaoBotCard):
    def __init__(self, thumbnail:str, title:str = None, desc:str = None):
        self.thumbnail = thumbnail
        self.title = title
        self.desc = desc
        self.buttons = []
        KakaoBotCard.__init__(self)
        return

    def AddButton(self, button:KakaoBotButton):
        self.buttons.append(button)
        return

    def GetName(self):
        return 'basicCard'

    def GetData(self):
        data = {}

        data['thumbnail'] = { 'imageUrl': self.thumbnail }
        if self.title:
            data['title'] = self.title
        if self.desc:
            data['description'] = self.desc

        buttons = []
        for b in self.buttons:
            buttons.append(b.GetData())

        if len(buttons):
            data['buttons'] = buttons

        return data

class KakaoBotCommerceCard(KakaoBotCard):
    def __init__(self):
        KakaoBotCard.__init__(self)
        return

    def GetName(self):
        return 'commerceCard'

class KakaoBotListCard(KakaoBotCard):
    def __init__(self):
        KakaoBotCard.__init__(self)
        return

    def GetName(self):
        return 'listCard'

class KakaoBotItemCard(KakaoBotCard):
    def __init__(self):
        KakaoBotCard.__init__(self)
        return

    def GetName(self):
        return 'itemCard'

class KakaoBotCarousel(KakaoBotOutput):
    def __init__(self):
        self.cards = []
        self.type = None
        KakaoBotOutput.__init__(self)
        return

    def SetHeader(self, thumbnail:str, title:str = None, desc:str = None):
        self.header = {}
        self.header['thumbnail'] = {'imageUrl' : thumbnail}
        if title:
            self.header['title'] = title
        if desc:
            self.header['description'] = desc
        return

    def AddCard(self, card:KakaoBotCard):
        if not self.cards:
            self.type = card.GetName()
        elif self.type != card.GetName():
            raise ValueError(
                'A carousel consists of only one type.(existing:%s, adding:%s)'
                % (self.type, card.GetName())
            )
        else:
            pass

        self.cards.append(card)
        return

    def GetName(self):
        return 'carousel'

    def GetData(self):
        if self.type is None:
            raise ValueError('A carousel has no inner card')

        items = []
        for c in self.cards:
            items.append(c.GetData())

        data = {
            'type': self.type,
            'items': items
        }

        if self.header is not None:
            data['header'] = self.header

        return data

class KakaoBotQuickReplies(KakaoBotOutput):
    def __init__(self):
        self.buttons = []
        KakaoBotCard.__init__(self)
        return

    def AddButton(self, button:KakaoBotBlockButton):
        self.buttons.append(button)
        return

    def GetName(self):
        return 'quickReplies'

    def GetData(self):
        items = []
        for b in self.buttons:
            items.append(b.GetData())
        return items