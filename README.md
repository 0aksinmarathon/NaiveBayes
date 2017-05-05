# NaiveBayes
# README #

対象サイト：https://gunosy.com/

### 開発環境 ###

+ OS
  * windows8


+ Python
  * Python 3.5
  * Django 1.10


+ 主な使用モジュール
  * urllib.request
  * bs4
  * janome
  * csv
  * collections
  * numpy
  * scrapy
  * tqdm



### NaiveBayesリポジトリ内の説明###

+ scrapy_gunosy
  * 学習データを上記対象サイトから記事をスクレーピング、
    記事のカテゴリ分類に対応したcsvファイルに記事を形態素解析し、名詞と判断されたものを
    各記事につき一行、の形式で書きこむ。


+ hello, mysite, templates, manage.py
  * Djangoフレームワークによるwebアプリケーションの実現する。
    送信フォームにgunosy.comの記事のURLを入力、送信することで
    学習データをもとにナイーブベイズ分類樹を用いた記事のカテゴリ分類を試みる。
  
+ precision_test.py
  * 上記分類の精度テストをコマンドプロンプト上で行う。
    各csvファイルの初めのn行(n記事分に相当)をそれぞれ学習データから消去したうえで
    分類器の引数として指定し、答え合わせをすることで正しく分類された割合を確認する。
    n = 30で精度約85.4%
  


