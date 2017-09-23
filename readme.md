## 機能
connpassで、キーワードに合致する今日以降に実施される東京開催のセミナーを監視して、
新着があったらslack, メールでお知らせ。

## 実行環境
- os不問
- python3


## インストール
- 必要なライブラリをpip、condaでインストール。（何のライブラリが必要かまでは書きません）
- 本モジュールは、任意のディレクトリに置けばよい。
- "(カレントディレクトリ：exec_main.pyがあるところ)/data" の中に、通知済み確認用の「past_articles.txt」というファイルが作成されます。存在しない場合は作成されます。   
past_articles.txtにないものは新着として扱われる為、past_articles.txtがない状態での初回実行時は、
実行日以降に開催される公開中のイベントは全て新着扱いになり、全て通知が配信されます。
メールは一通のみですが、Slackは大量の通知が発生します。  
もしそれを避けたい場合は、DEBUG=Trueとして実行してpast_articles.txtを作成し、
その後はDEBUG=Falseに切り替えておけば、新たに公開されたもののみが新着として扱われます。


## 設定すべきパラメータ
- exec_main.py
	- `SLEEP_MIN` : チェックを行う間隔。（分）
    - `DEBUG` : デバッグモード。メール、slack配信はしない。 /data/checklist.txt は更新する。
- ./settings/target.py
    - 監視対象のキーワード。空白は＋でつなぐ。例：`deep+learning`
- ./settings/private.py
    git対象外の設定ファイル。private_sample.pyを参考に。


## 実行方法
   ターミナル、コマンドプロンプトで、 `python exec_main.py`　と入力、実行。




## 今後やりたいこと
- AWS Lamda + DynamoDB に移行
- ユーザー個別の設定、配信
  自分が登録したキーワードに新着があったら、Slackに通知(「@xxx 新着があります[....]」)   
  現在URLのみの通知に、@user を追加しても良い。
- ATND, doorkeepr, dots等の他のサイトも監視
- API化
    参考
    http://qiita.com/kiida/items/373446edd2fb09da82ca
- 金融庁、日銀、経産省などのお知らせも同様に監視
