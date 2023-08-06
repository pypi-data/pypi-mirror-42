"""Yo! Here, there are python representations of the Telegram bot API objects"""

# pylint: disable=too-few-public-methods


class Chat:
    """Represents telegram chat info, typically referenced by messages"""
    def __init__(self, cid, first_name, ctype):
        """Instanciates a chat"""
        self.cid = cid
        self.first_name = first_name
        self.ctype = ctype


class Message:
    """Represents telegram messages, typically contained in updates"""
    def __init__(self, mid, mfrom, chat, date, text):  # pylint: disable=too-many-arguments
        """Instanciates a message"""
        self.mid = mid
        self.mfrom = mfrom
        self.chat = chat
        self.date = date
        self.text = text


class Update:
    """Represents telegram updates, which is what you will most likely be working with"""
    def __init__(self, uid, message):
        """Instanciates an update"""
        self.uid = uid
        self.message = message
