

# **参考** : [connpass APIリファレンス](https://connpass.com/about/api/)
# 


import requests
import json
import datetime
import time
import random
import math
# 年、月の計算はこれが必要。datetimeでは出来ない。
from dateutil.relativedelta import relativedelta

#  一時的にWIPフォルダでやっているから、一個上のディレクトリに抜ける必要がある。
#  ちゃんと本体に組み込む時には不要。
import sys
sys.path.append('..')

# 自作
from settings import target



# API検索条件 ####################################
# 開催場所
location = '東京都'
# 検索キーワード(or)
# 検索結果が500を超えた分は、結果を取得できない。
# キーワードをシャッフルして、検索結果数に偏りが内容にしようとする気休め。
search_words = target.SEARCH_WORDS
random.shuffle(search_words)
# 今月を含め、何ヶ月先まで検索するか
search_months = 3
# 一度に取得するデータ件数。100で良い。（最小1, 最大100。apiの仕様。）
nb_get_data = 100

# システム設定 ###################################
# エンドポイント
url = 'https://connpass.com/api/v1/event/'
# 一度に検索するキーワード数（検索結果が多すぎるとエラー）。実績値で40程度。
# 小さすぎると検索回数が増える。一度、アクセス過多で運営から注意を受けているので気をつかう。
nb_search_words = min(math.ceil(len(search_words) / 2), 40)
# get失敗時に中断するか(boolean)
continue_on_error = False
# リクエスト連投で空けるべき時間（秒）。１秒以上。
request_sleep_sec = 2


def get_response(url, params):
    """
    リクエストを投げて、レスポンスを受け取る。
    リクエストは必ずこの関数を使用することで、sleepを保証する。
    """
    time.sleep(request_sleep_sec)
    return requests.get(url, params=params)


def get_search_result(start, batch_start):
    q = {'count': nb_get_data,   # 取得件数
         'start': start,         # 検索の開始位置。結果セットを複数回に分けて取得しないといけないので。
         'ym': ym ,              # イベント開催年月
         'keyword': location,    #  キーワード (AND)
         'keyword_or': target.SEARCH_WORDS[batch_start: batch_start + nb_search_words]  # キーワード (OR)
        }
    return get_response(url, params=q)


# 検索対象月のリスト作成
ym = [(datetime.date.today() + relativedelta(months=i)).strftime('%Y%m')
      for i in range(search_months)]

today = datetime.datetime.today()
# 結果セット全体の中での処理開始位置
for batch_start in list(range(len(search_words)))[: : nb_search_words]:
    print('*' * 10, 'batch_start :', batch_start, '*' * 100)
    start = 1
    nb_all_result = sys.maxsize     # 後で更新
    while start < nb_all_result:
        r = get_search_result(start, batch_start)
        # エラーチェック
        if not r.ok:
            if continue_on_error:
                print('APIからのGETに失敗: [{}] {}'.format(r.status_code, r.reason))
                print('エラーでも中断しない設定なので、監視を続けます。')
                continue
            else:
                assert r.ok, 'APIからのGETに失敗: [{}] {}'.format(r.status_code, r.reason)
        
        # 大した処理ではないので、わかりやすさを優先して、リスト内包表記は使用しない
        for event in r.json()['events']:
            event_datetime = datetime.datetime.strptime(event['started_at'][:-6], '%Y-%m-%dT%H:%M:%S')
            if today <= event_datetime:
                print( event_datetime, event['title'], event['event_url'])

        start += int(r.json()['results_returned'])
        nb_all_result = int(r.json()['results_available'])   # 同じキーワードなら、連続して検索しても同じ
