# keach

## 初期化
1. python3 setup_database.py でデータベースを作成する
2. python3 average_document.py seed_url_list で平均文書を作成する
2. crawler.py seed_url_list でクローラを走らせる
3. python3 flask_main.py で http://localhost:5000/ にアプリケーションが開く

## Todo
1. 言語判定を行う
2. プロセス並列化によるクローラの高速化
3. Mecab?を使った日本語対応
4. tfidf以外の優先度の導入。単語の共起確率をまともだと考えられる文書と比べる。
5. Pagerankの導入
6. tfidfテーブルの圧縮
7. html以外のコンテンツを弾く
8. 結果からJaveScriptの部分を除く
9. アクセスログを取る
10. クローラの優先度をアクセスログにしたがって変える
11. pdfファイルに対応する
12. クロールするドメインにできるだけ多様性をもたせる
13. クローラの高速化。不要なファイルをダウンロードしないとか。

## Done
1. readbilityを使った本文取得の高速化
