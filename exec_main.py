# coding=utf-8

"""
セミナー情報などを監視し、新規に公開されたものがあったら、
メール・slackで通知する。

このスクリプトを実行する。
"""
from pathlib import Path

import re
import time
import datetime

# 自作

from connpass import ConnpassApi
from post2slack import Post2Slack

##################################################################
SLEEP_MIN = 8       # チェックする間隔（分）
DEBUG = False        # デバッグモード True/False
PAST_ARTICLES_FILE = './data/past_articles.txt'     # 通知済みリスト。新着チェック用。
SLACK_CHANNEL = 'セミナー情報'  #seminor, bot_test, sandbox
##################################################################

def debug_print(msg):
    if DEBUG:
        print(msg)

if __name__ == "__main__":
    today = datetime.date.today().strftime('%Y/%m/%d')


    # 前回までの取得データを読み込み
    checkset = set()
    p = Path(PAST_ARTICLES_FILE)
    if p.exists():
        with open(PAST_ARTICLES_FILE, mode='r', encoding='utf-8') as f:
            for f_line in f:
                f_line = re.sub(r'[\n]', '', f_line)
                print(f_line)
                checkset.add(f_line)

    # Slack投稿用インスタンス
    slack = Post2Slack()
    # connpassデータ取得用インスタンス
    cp = ConnpassApi()

    while True:
        start_time = time.time()
        maillist = ''
        urllist = []

        # connpassのデータを取得
        result = cp.get_all_result()
        if result['status']['ok']:
            all_events = result['events']
        else:
            print('APIでエラー : [{}] {}'.format(result['status']['status_code'], result['status']['reason']))
            # slackに通知するとエラーが出続ける。でも多分日をまたぐとか時間をおくとエラーは解消するので、停止したくない。
            # todo 今後わかるようにしたい。

        # 配信済みリストと照らしあわせて、なかったら新着とする
        for event_date, event_title, event_url in all_events:
            checkstring = event_date[:-9] + '  ' + event_title
            if checkstring not in checkset:
                print('新着: ', checkstring)
                with open(PAST_ARTICLES_FILE, mode='a', encoding='utf-8') as f:
                    f.write(checkstring + '\n')
                checkset.add(checkstring)
                maillist = maillist + ('* ' + event_title + '\n\n')
                urllist.append(event_url)

        if len(maillist) != 0:
            if DEBUG:
                debug_print(maillist)
            else:
                # メールに飛ばす
                # sendmail.send_mail('新着セミナー', maillist)
                # slackにも飛ばす
                for url in urllist:
                    slack.post_message_to_channel(message=url,
                                                  channel_name=SLACK_CHANNEL,
                                                  icon_emoji=':loudspeaker:',
                                                  username='セミナー速報')

        debug_print('★★★★★★ {} ★★★★★★'.format('デバッグモード中です！'))
        elapsed_time = time.time() - start_time
        print('--------------------- {0} (elapsed time : {1:.2f}分) --------------------'
              .format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M'),
                      elapsed_time / 60))

        time.sleep(SLEEP_MIN * 60)
