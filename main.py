# coding=utf-8

"""
セミナー情報などを監視し、新規に公開されたものがあったら、
メール・slackで通知する。

このスクリプトを実行する。
"""

import requests
from bs4 import BeautifulSoup
import csv
import re
import time
import datetime
import os.path
import sendmail     # オリジナル

# from slackbot.bot import Bot
from slacker import Slacker
from setting import target
# Git管理対象外
from setting import private


##################################################################
SLEEP_MIN = 3       # チェックする間隔（分）
NB_GETPAGES = 10     # スクレイピングするページ数。せいぜい１０ページ。
<<<<<<< HEAD
DEBUG = False        # デバッグモード
=======
DEBUG = False        # デバッグモード True/False
>>>>>>> なんか

##################################################################

class Slack(object):
    __slacker = None

    def __init__(self, token):
        self.__slacker = Slacker(token)


    def post_message_to_channel(self, channel, message, attachments=None):
        """
        Slackチームの任意のチャンネルにメッセージを投稿する。
        """
        channel_name = "#" + channel
        self.__slacker.chat.post_message(channel_name, message,
                                         icon_emoji=':loudspeaker:',
                                         username='セミナー速報（テスト配信中）',
                                         unfurl_links=True,
                                         attachments=attachments
                                         )


def debug_print(msg):
    if DEBUG:
        print(msg)

if __name__ == "__main__":
    today = datetime.date.today().strftime('%Y/%m/%d')
    check_file = './data/checklist.txt'

    slack = Slack(private.SLACK_API_TOKEN)

    # 前回までの取得データを読み込み
    checkset = set()
    if os.path.isfile(check_file):
        with open(check_file, mode='r', encoding='utf-8') as f:
            for f_line in f:
                f_line = re.sub(r'[\n]', '', f_line)
                print(f_line)
                checkset.add(f_line)


    while True:
        start_time = time.time()
        maillist = ''
        urllist = []
        with open(check_file, mode='a', encoding='utf-8') as f:
            for page in range(NB_GETPAGES):
                for word in target.SEARCH_WORDS:
                    urlst = ('https://connpass.com/search/?page={0}&q={1}&start_from={2}&'
                             'start_to=&prefectures=tokyo&selectItem=tokyo'.format(page, word, today))

                    # print(urlst)
                    htmlPage = requests.get(urlst)
                    soup = BeautifulSoup(htmlPage.content, 'html.parser')
                    # try:
                    events = soup.find_all(class_='event_list vevent')
                    #     print('無効：' + url)
                    debug_print('----------------- search word : {0}({1}ページ目 - {2}件)'.format(word, page + 1, len(events)))
                    if len(events) == 0:
                        continue
                    else:
                        for event in events:
                             # Define label based on the stars given to the review
                            event_title = event.find('a', {'class':'url summary'}).get_text()
                            event_url = event.find('a', {'class':'url summary'}).get("href")
                            # 改行とカンマを置換
                            event_title = re.sub(r'[\n,]', ' ', event_title)
                            event_date = event.find('p', {'class':'year'}).get_text() + '/' + \
                                event.find('p', {'class':'date'}).get_text()
                            checkstring = event_date + '  ' + event_title
                            if checkstring not in checkset:
                                print('新着: ', checkstring)
                                checkset.add(checkstring)
                                f.write(checkstring + '\n')
                                maillist = maillist + ('* ' + event_title + '\n\n')
                                urllist.append(event_url)

        if len(maillist) != 0:
            if DEBUG:
                debug_print(maillist)
            else:
                # メールに飛ばす
                sendmail.send_mail('新着セミナー', maillist)
                # slackにも飛ばす
                for url in urllist:
                    slack.post_message_to_channel(private.SLACK_CHANNEL, url)

        debug_print('★★★★★★ {} ★★★★★★'.format('デバッグモード中です！'))
        elapsed_time = time.time() - start_time
        print('--------------------- {0} (elapsed time : {1:.2f}分) --------------------'
              .format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M'),
                      elapsed_time / 60))
        time.sleep(SLEEP_MIN * 60)
