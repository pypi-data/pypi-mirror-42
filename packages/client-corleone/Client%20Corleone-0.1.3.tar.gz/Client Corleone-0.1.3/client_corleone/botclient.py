import logging
import requests
import time

from client_corleone.serializers import UpdateSerializer


logger = logging.getLogger('client')


class BotClient:
    def __init__(self, token, max_retries=None):
        self.bot_url = f'https://api.telegram.org/bot{token}'
        self.max_retries = max_retries

    def updates(self):
        offset = 0
        retries = self.max_retries

        while True:
            try:
                raw_updates = requests.get(f'{self.bot_url}/getUpdates?offset={offset}').json()
                if not raw_updates.get('ok'):
                    logger.error('Updates NOK')
                    raise ConnectionError('Updates NOK')
            except ConnectionError:
                logger.error('Connection error')
                if retries:
                    retries -= 1
                    # Waits: 1s, 2s, 4s, 8s...
                    time.sleep((self.max_retries - retries) ** 2)
                    continue
                return

            retries = self.max_retries

            updates = UpdateSerializer(raw_updates['result'], many=True).data

            for update in updates:
                yield update
                offset = update.uid + 1

    def send_text(self, chat_id, text):
        requests.post(f'{self.bot_url}/sendMessage', data={'chat_id': chat_id, 'text': text})
