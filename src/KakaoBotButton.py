# -*- coding: utf-8 -*-

class KakaoBotButton:
    def __init__(self, label:str, extra:dict = None):
        self.label = label
        self.extra = extra
        return

    def GetData(self):
        raise NotImplementedError('KakaoBotButton.GetData method must be called after impement by a derived class.')

class KakaoBotMsgButton(KakaoBotButton):
    def __init__(self, label:str, msg:str, extra:dict = None):
        self.action = 'message'
        self.msg = msg
        KakaoBotButton.__init__(self, label, extra)
        return

    def GetData(self):
        return {
            'action': self.action,
            'label': self.label,
            'messageText': self.msg
        }

class KakaoBotLinkButton(KakaoBotButton):
    def __init__(self, label:str, url:str, extra:dict = None):
        self.action = 'webLink'
        self.url = url
        KakaoBotButton.__init__(self, label, extra)
        return

    def GetData(self):
        return {
            'action': self.action,
            'label': self.label,
            'webLinkUrl': self.url
        }

class KakaoBotPhoneButton(KakaoBotButton):
    def __init__(self, label:str, phone:str, extra:dict = None):
        self.action = 'phone'
        self.phone = phone
        KakaoBotButton.__init__(self, label, extra)
        return

    def GetData(self):
        return {
            'action': self.action,
            'label': self.label,
            'phoneNumber': self.phone
        }

class KakaoBotBlockButton(KakaoBotButton):
    def __init__(self, label:str, text:str, blockId:str, extra:dict = None):
        self.action = 'block'
        self.text = text
        self.blockId = blockId
        KakaoBotButton.__init__(self, label, extra)
        return

    def GetData(self):
        return {
            'action': self.action,
            'label': self.label,
            'messageText': self.text,
            'blockId': self.blockId
        }
