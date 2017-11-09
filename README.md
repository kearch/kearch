# keach

## 初期化
1. python3 setup_database.py でデータベースを作成する
2. python3 average_document.py seed_url_list で平均文書を作成する
3. python3 crawler.py seed_url_list でクローラを走らせる
4. python3 flask_main.py で http://localhost:5000/ にアプリケーションが開く

## Todo
8. 結果からJaveScriptの部分を除く
18. ページのダウンロードに時間制限を設ける
1. 言語判定を行う
3. Mecab?を使った日本語対応
4. tfidf以外の優先度の導入。単語の共起確率を用いてまともだと考えられる文書と比べる。
5. Pagerankの導入
7. html以外のコンテンツを弾く
9. アクセスログを取る
10. クローラの優先度をアクセスログにしたがって変える
11. pdfファイルに対応する
13. クローラの高速化。不要なファイルをダウンロードしないとか。
14. JaveScriptをscriptタグを検出して除く
15. linkをInt型に変換してデータベースに保存する
20. 複数INSERTをまとめる
21. insert処理が遅すぎる
    indexを外してinsertしたうえでindex構築する必要がある

## Done
1. readbilityを使った本文取得の高速化
2. とりあえずpdfは弾いた
2. プロセス並列化によるクローラの高速化
6. tfidfテーブルの圧縮（登録する単語を一ページあたり上位100語に限定)
16. png,jpg,PDF,jsonを弾いた
19. crawlerテーブルはurl indexedのものとlast_date indexedのものの2つを作り検索の高速化をする
17. 同一ドメインへの連続アクセスを避ける  
last_dateに乱数を足して対応  
12. クロールするドメインにできるだけ多様性をもたせる  
last_dateに乱数を足して対応  

## クローラの速度
今のところ1second/1pageぐらい
