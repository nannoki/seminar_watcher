## 機能
connpassで、キーワードに合致する今日以降に実施される東京開催のセミナーを監視して、
新着があったらslack, メールでお知らせ。

## 実行環境
- os不問
- python3
- 必要なライブラリ
（どれが追加インストールが必要か管理していなかったので、他にあるかも。逆に標で入っているかも。importのところを見れば必要なものはわかる。）
	- requests
	- BeautifulSoup4
	- smtplib
	- email

## インストール
- 上記ライブラリをpip、condaでインストール。
- 本モジュールは、任意のディレクトリに置けばよい。
- "(カレントディレクトリ：main.pyがあるところ)/data" の中に、通知済み確認用の「checklist.txt」というファイルが作成されます。存在しない場合は作成されます。   
checklist.txtにないものは新着として扱われる為、checklist.txtがない状態での初回実行時は、
実行日以降に開催される公開中のイベントは全て新着扱いになり、全て通知が配信されます。
メールは一通のみですが、Slackは大量の通知が発生します。  
もしそれを避けたい場合は、DEBUG=Trueとして一度実行するとchecklist.txtが作成される為、
その後は新たに公開されたもののみが新着として扱われます。


## 設定すべきパラメータ
- main.py
	- `SLEEP_MIN` : チェックを行う間隔。（分）
    - `NB_GETPAGES` : スクレイピングするページ数。
    - `DEBUG` : デバッグモード。メール、slack配信はしない。 /data/checklist.txt は更新する。
- ./setting/target.py
    - 監視対象のキーワード。空白は＋でつなぐ。例：`deep+learning`
- ./setting/private.py
    このファイルは個人設定を含む為、git管理対象外。private_sample.pyを参考に。
    - `FROMADDRESS` : 送信元メールアドレス。
    - `PW` : 送信者のパスワード
    - `TOADDRESS` : 送信先メールアドレス。社外OK。
    - `SMTPSV` : smtpサーバ。
    - `SLACK_API_TOKEN` : Slack APIのアクセストークン
    - `SLACK_CHANNEL` : 投稿先のchannel名
    - `SLACK_CHANNEL_TEST` : テスト投稿先のchannel名。test_slack.pyを使用する時のみ。


## 実行方法
   ターミナル、コマンドプロンプトで、 `python main.py`　と入力、実行。


## 今後やりたいこと
- AWS Lamda + DynamoDB に移行
- GitHubの公開リポジトリに移行し、コントリビュータにフォークして開発してもらう。
- ユーザー個別の設定、配信
  自分が登録したキーワードに新着があったら、Slackに通知(「@xxx 新着があります[....]」)   
  現在URLのみの通知に、@user を追加しても良い。
- ATND, doorkeepr, dots等の他のサイトも監視
- API化
    参考
    http://qiita.com/kiida/items/373446edd2fb09da82ca
- 金融庁、日銀、経産省などのお知らせも同様に監視
