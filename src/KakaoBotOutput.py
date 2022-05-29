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
        self.head = None
        self.imageTitle = None
        self.title = None
        self.desc = None
        self.thumbnail = None
        self.profile = None
        self.items = []
        self.itemAlign = None
        self.itemSummary = None
        self.buttons = []
        self.buttonLayout = None
        return

    def SetHead(self, title:str):
        self.head = { 'title' : title }
        return

    def SetTitle(self, title:str=None):
        self.title = title
        return

    def SetDesc(self, desc:str=None):
        self.desc = desc
        return

    def SetProfile(self, title:str, url:str = '', width:int = -1, height:int = -1):
        self.profile= { 'title' : title }
        if len(url):
            self.profile['imageUrl'] = url
        if width != -1:
            self.profile['width'] = width
        if height != -1:
            self.profile['height'] = height
        return

    def SetThumbnail(self, url:str, width:int, height:int):
        self.thumbnail = {
            'imageUrl' : url,
            'width'    : width,
            'height'   : height,
        }
        return
    def SetImageTitle(self, title:str=None, desc:str=None):
        self.imageTitle = { 'title' : title, 'description' : desc }
        return

    def SetItemListAlignment(self, align:str):
        if align not in ['left', 'right']:
            raise ValueError('Invalid option for ItemCard.SetItemListAlignment.')
        self.itemAlign = align
        return

    def SetItemListSummary(self, title:str, desc:str):
        self.itemSummary= { 'title' : title, 'description' : desc }
        return

    def AddItem(self, title:str, desc:str):
        self.items.append({'title':title, 'description':desc})
        return

    def SetButtonLayout(self, layout:str):
        if layout not in ['horizontal', 'vertical']:
            raise ValueError('Invalid option for ItemCard.SetButtonLayout.')
        self.buttonLayout = layout
        return

    def AddButton(self, button:KakaoBotButton):
        if len(self.buttons) == 3:
            raise ValueError('Too many ItemCard is added.(max: 3 buttons)')
        self.buttons.append(button)
        return

    def GetName(self):
        return 'itemCard'

    def GetData(self):
        data = {}

        if self.head:
            data['head'] = self.head
        if self.title:
            data['title'] = self.title
        if self.desc:
            data['description'] = self.desc
        if self.profile:
            data['profile'] = self.profile

        if self.thumbnail:
            data['thumbnail'] = self.thumbnail
            if self.imageTitle:
                data['imageTitle'] = self.imageTitle

        if self.itemAlign:
            data['itemListAlignment'] = self.itemAlign
        if self.itemSummary:
            data['itemListSummary'] = self.itemSummary
        if self.items:
            data['itemList'] = self.items

        if self.buttons:
            data['buttons'] = [b.GetData() for b in self.buttons]
        if self.buttonLayout and len(self.buttons) <= 2:
            data['buttonLayout'] = self.buttonLayout

        return data

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
