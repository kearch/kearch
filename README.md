# keach

## 初期化
1. python3 setup_database.py でデータベースを作成する
2. python3 average_document.py seed_url_list で平均文書を作成する
3. python3 lda_topic_detect.py computer_science_url_list random_url_list で分類器を作成する
4. python3 crawler.py seed_url_list でクローラを走らせる
5. python3 flask_main.py で http://localhost:5000/ にアプリケーションが開く
6. ssh -f -N itokawa -L 5000:itokawa:5000 で外部からアプリケーションをlocalhost:5000で見れるようになる

## 目標
- クローリング速度0.1second/page
- 保存ページ数1000万ページ
- 10日ぐらいでindexの中のすべてのページを更新
- twitterや2chなどの価値の少ない情報、時代によって価値の変わりやすい情報を保持しない
- pagerankでページに順位をつける
- 複数の領域特化検索エンジンをマスター/スレイブ形式で接続することで、より大きな検索エンジンを構成する

## Todo
- 英語以外の文字にもちゃんと対応する
- Mecab?を使った日本語対応
- tfidf以外の優先度の導入。単語の共起確率を用いてまともだと考えられる文書と比べる。
- html以外のコンテンツを弾く
- アクセスログを取る
- クローラの優先度をアクセスログにしたがって変える
- pdfファイルに対応する
- クローラの高速化。不要なファイルをダウンロードしないとか。
- linkをInt型に変換してデータベースに保存する
- insert処理が遅すぎる
  indexを外してinsertしたうえでindex構築する必要がある

## Done
- タイトルの情報を使う
- Pagerankを表示に反映する
    - ウェブページの評価関数はページランクとtfidfの積になりました
- Pagerankの導入
    - まずすべてのページのスコアを1にする。このテーブルをpagerank_now とする
    - 新しくページをクロールするときにその派生リンクについて、リンクにpagerank_now のスコアを加える  
      ただし実際にupdate すると遅いのでinsert にしておく
      これをpagerank_next とする
    - クロールが終わったらpagerank_next を集計してpagerank_now と入れ替える
- LDA topic model + SGD classifier を用いたクラスタ分類
  https://www.slideshare.net/tsubosaka/tokyotextmining
- Computer Science に関する記事を100本、それ以外の記事を100本記録する
- readbilityを使った本文取得の高速化
- とりあえずpdfは弾いた
- プロセス並列化によるクローラの高速化
- tfidfテーブルの圧縮（登録する単語を一ページあたり上位100語に限定)
- png,jpg,PDF,jsonを弾いた
- crawlerテーブルはurl indexedのものとlast_date indexedのものの2つを作り検索の高速化をする
- 同一ドメインへの連続アクセスを避ける  
  last_dateに乱数を足して対応  
- クロールするドメインにできるだけ多様性をもたせる  
  last_dateに乱数を足して対応  
- ページのダウンロードに時間制限を設ける
  register処理にも時間制限を設けた
- 複数INSERTをまとめる
  やったけどあんまり効果なし
- 結果からJaveScriptの部分を除く
- 言語判定を行う
  http://lab.astamuse.co.jp/entry/try-polyglot
- JaveScriptをscriptタグを検出して除く
- 外部サイトへのリンクを重要視する

## クローラの速度
今のところ1second/1pageぐらい
