
import sys
import requests
import datetime
import time
import random
# 年、月の計算はこれが必要。datetimeでは出来ない。
from dateutil.relativedelta import relativedelta

# 自作
from settings import target

class ConnpassApi:
    def __init__(self):
        # エンドポイント
        self.url = 'https://connpass.com/api/v1/event/'


        # API検索条件 ####################################
        # 開催場所
        self.location = '東京都'
        # 検索キーワード(or)
        # 検索結果が500を超えた分は、結果を取得できない。
        # キーワードをシャッフルして、検索結果数に偏りが内容にしようとする気休め。
        self.search_words = target.SEARCH_WORDS
        random.shuffle(self.search_words)
        # 今月を含め、何ヶ月先まで検索するか
        self.search_months = 3
        # 一度に取得するデータ件数。100で良い。（最小1, 最大100。apiの仕様。）
        self.n_get_data = 100

        # システム設定 ###################################
        # 一度に検索するキーワード数（検索結果が多すぎるとエラーになることがあった）。40を超えると怪しい。
        self.batch_size = 20
        # リクエスト連投で空ける時間（秒）。１秒以上。
        self.request_sleep_sec = 3

        # get失敗時に中断するか(boolean)
        # self.continue_on_error = False


    def _get_response(self, url, params):
        """
        リクエストを投げて、レスポンスを受け取る。
        リクエストは必ずこの関数を使用することで、sleepを保証する。
        """
        time.sleep(self.request_sleep_sec)
        return requests.get(url, params=params)


    def _get_search_result(self, start, ym, batch_start):
        q = {'count': self.n_get_data,  # 取得件数
             'start': start,  # 検索の開始位置。結果セットを複数回に分けて取得しないといけないので。
             'ym': ym ,  # イベント開催年月
             'keyword': self.location,  #  キーワード (AND)
             'keyword_or': target.SEARCH_WORDS[batch_start: batch_start + self.batch_size]  # キーワード (OR)
             }
        return self._get_response(self.url, params=q)


    def get_all_result(self):

        # 検索対象月のリスト作成。ずっと動かし続けるので、日付は毎回取得。
        today = datetime.datetime.today()
        ym = [(today + relativedelta(months=i)).strftime('%Y%m')
              for i in range(self.search_months)]

        all_events = []
        # 結果セット全体の中での処理開始位置
        for batch_start in list(range(len(self.search_words)))[: : self.batch_size]:
            start = 1
            n_all_result = sys.maxsize     # 後で更新
            while start < n_all_result:
                r = self._get_search_result(start, ym, batch_start)
                # エラーチェック
                if r.ok:
                    for event in r.json()['events']:
                        event_datetime = datetime.datetime.strptime(event['started_at'][:-6], '%Y-%m-%dT%H:%M:%S')
                        if today <= event_datetime:
                            all_events.append([event['started_at'], event['title'], event['event_url']])

                    # all_events.append(
                    #     [event['started_at'], event['title'], event['event_url']]
                    #      for event in r.json()['events']
                    #      if today <= datetime.datetime.strptime(event['started_at'][:-6], '%Y-%m-%dT%H:%M:%S')])

                    start += int(r.json()['results_returned'])
                    n_all_result = int(r.json()['results_available'])   # 同じキーワードなら、連続して検索しても同じ
                else:
                    break

            return {'status': {'ok': r.ok, 'status_code': r.status_code, 'reason': r.reason},
                'events': all_events}


if __name__ == '__main__':
    cp = ConnpassApi()
    cp.get_all_result()



