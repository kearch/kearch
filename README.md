# keach

## 初期化
1. python3 setup_database.py でデータベースを作成する
2. python3 average_document.py seed_url_list で平均文書を作成する
2. crawler.py seed_url_list でクローラを走らせる
3. python3 flask_main.py で http://localhost:5000/ にアプリケーションが開く

## Todo
1. readbilityを使った本文取得の高速化
2. プロセス並列化によるクローラの高速化
3. 言語判定を行う
4. Mecab?を使った日本語対応
5. tfidf以外の優先度の導入。単語の共起確率をまともだと考えられる文書と比べる。
6. Pagerankの導入
7. tfidfテーブルの圧縮
