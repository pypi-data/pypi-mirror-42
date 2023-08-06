from abc import abstractmethod

from client_corleone.models import Chat, Message, Update


class Serializer:
    @property
    def data(self):
        result = [self.serialize(datum) for datum in self._raw_data]
        return result if self.many else result[0]

    @abstractmethod
    def serialize(self, raw_data):
        pass

    def __init__(self, raw_data, many=False):
        self.many = many
        self._raw_data = raw_data if many else [raw_data]


class UpdateSerializer(Serializer):
    def serialize(self, raw_data):
        message = MessageSerializer(raw_data['message']).data
        return Update(raw_data['update_id'], message)


class MessageSerializer(Serializer):
    def serialize(self, raw_data):
        chat = ChatSerializer(raw_data['chat']).data
        return Message(
            raw_data['message_id'], raw_data['from'],
            chat, raw_data['date'], raw_data['text']
        )


class ChatSerializer(Serializer):
    def serialize(self, raw_data):
        return Chat(cid=raw_data['id'], first_name=raw_data['first_name'], ctype=raw_data['type'])
