"""This is the main entrypoint of client_corleone it contains the BotClient
class that will allow you to receive updates from your telegram bot
in a pythonic style."""
import logging
import time

import requests

from client_corleone.serializers import UpdateSerializer


LOGGER = logging.getLogger('client')


class BotClient:
    """This class allows you to get udpates from your bot, as well as send messages through it."""
    def __init__(self, token, max_retries=None):
        """Token is the one the bot father gave you
        max_retries will give you the oportunity to call again your bot, first 1s, then 2, 4, 8...
        up to n^2, indeed, don't set the bar too high, for you will regret it.
        """
        self.bot_url = f'https://api.telegram.org/bot{token}'
        self.max_retries = max_retries

    def updates(self):
        """Returns a generator. It contains an infinite loop, don't try to do fancy style like
        list(client.updates(), for you will wait like forever to get it done.

        You are supposed to use it as:

        for update in client.updates:
            Do the stuff
        """
        offset = 0
        retries = self.max_retries

        while True:
            try:
                raw_updates = requests.get(f'{self.bot_url}/getUpdates?offset={offset}').json()
                if not raw_updates.get('ok'):
                    LOGGER.error('Updates NOK')
                    raise ConnectionError('Updates NOK')
            except ConnectionError:
                LOGGER.error('Connection error')
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
        """Send a message with the given text to the chat identified by chat_id"""
        requests.post(f'{self.bot_url}/sendMessage', data={'chat_id': chat_id, 'text': text})
