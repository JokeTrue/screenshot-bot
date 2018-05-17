import os
import re
import time
import uuid
from contextlib import suppress
from os.path import join

import telepot
import urllib3
from telepot.loop import MessageLoop

from conf.utils import tor_driver
from settings import TOKEN, MEDIA_PATH

proxy_url = "http://104.236.4.72:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (
    urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

NOT_URL = 0
SCREENSHOT_ERROR = 1
START_LOADING = 2

ANSWERS = {
    NOT_URL: "Send me a valid URL",
    SCREENSHOT_ERROR: 'Error while taking a screenshot',
    START_LOADING: "Started loading a screenshot..."
}

URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://' 
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
    r'(?::\d+)?' 
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

tor_driver = tor_driver()


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        if re.match(URL_REGEX, msg['text']):
            bot.sendMessage(chat_id, ANSWERS[START_LOADING])
            url = re.findall(URL_REGEX, msg['text'])[0]

            out_img_path = join(MEDIA_PATH, '{}.png'.format(uuid.uuid4().hex))

            try:
                with tor_driver as driver:
                    driver.get(url)
                    driver.get_screenshot_as_file(out_img_path)

                with open(out_img_path, 'rb') as screenshot:
                    bot.sendPhoto(chat_id, screenshot)

            except Exception as e:
                bot.sendMessage(chat_id, ANSWERS[SCREENSHOT_ERROR])

            finally:
                with suppress(OSError):
                    os.remove(out_img_path)

        else:
            bot.sendMessage(chat_id, ANSWERS[NOT_URL])


bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)
