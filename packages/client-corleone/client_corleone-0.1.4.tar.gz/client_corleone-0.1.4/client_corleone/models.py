class Chat:
    def __init__(self, cid, first_name, ctype):
        self.cid = cid
        self.first_name = first_name
        self.ctype = ctype


class Message:
    def __init__(self, mid, mfrom, chat, date, text):
        self.mid = mid
        self.mfrom = mfrom
        self.chat = chat
        self.date = date
        self.text = text


class Update:
    def __init__(self, uid, message):
        self.uid = uid
        self.message = message
