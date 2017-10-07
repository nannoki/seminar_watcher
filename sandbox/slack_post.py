# coding=utf-8

"""
セミナー情報などを監視し、新規に公開されたものがあったら、
メール・slackで通知する。

このスクリプトを実行する。
"""

from slacker import Slacker
from settings import post2slack_private as setting

import sys
sys.path.append('../')

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

    slack = Slack(setting.API_TOKEN)

    msg = 'pythonからの投稿テスト'
    attachments = {}

    slack.post_message_to_channel(setting.DEFAULT_CHANNEL, msg, attachments)
    print('メッセージをslackに投稿しました : [{}]'.format(msg))
