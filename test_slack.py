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
DEBUG = True        # デバッグモード

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
                                         username='（テスト中）',
                                         unfurl_links=True,
                                         attachments=attachments
                                         )


if __name__ == "__main__":


    slack = Slack(private.SLACK_API_TOKEN)

    msg = 'pythonからの投稿テスト'
    attachments = {}

    slack.post_message_to_channel(private.SLACK_CHANNEL_TEST, msg, attachments)
    print('メッセージをslackに投稿しました : [{}]'.format(msg))
