# -*-  coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.shortcuts import render
from urllib.request import urlopen
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
import csv
import collections as col
import numpy as np

def NBClassify(request):
    """
    ナイーブベイズの手法を用いて 入力されたURLのページを分類する
    """

    if request.GET.get('URL'):
        #取得URLの文章を形態素解析し、名詞のみにしたものをリストとして抽出
        article_wordlist = make_article_wordlist(request.GET.get('URL'))

        #csvファイルから学習データを読み込み
        train_data, category_document_number = draw_train_data_from_csv()

        #取得URLの記事が各カテゴリに属する事後確率を対数にしたものをリストの形で取得
        log_post_prob_list = calculate_post_prob(train_data, article_wordlist, category_document_number)

        #事後確率が最大のカテゴリをページに出力
        number_to_category = {0: "エンタメ", 1: "スポーツ", 2:"おもしろ", 3:"国内", 4: "海外", 5: "コラム", 6: "IT・科学", 7: "グルメ"}
        d = {
            'category': number_to_category[log_post_prob_list.index(max(log_post_prob_list))]  #number_to_category[log_count_list.index(max(log_count_list))]
        }

        return render(request, 'index.html', d)
    else:
        return render(request, 'index.html', {'category': ""})




def make_article_wordlist(requested_url):
    """
    取得URLの文章を形態素解析し、名詞のみにしたものをリストとして抽出
    """
    #取得URLの文章を抽出
    html = urlopen(requested_url)
    bsobj = BeautifulSoup(html, 'html.parser')
    article_objects = list(bsobj.findAll(class_="article"))
    article_wordlist_before_processed = []
    for i in article_objects:
        article_wordlist_before_processed.append(i.get_text())
    joined_article_wordlist_before_processed = "".join(article_wordlist_before_processed)

    #名詞でかつNG文字を含まないもののみを抽出、リストの形で返す
    ngwords = ["(", ")", "（", "）", "[", "]", "{", "}", "１", "２", "３", "４", "５", "６", "７", "８",
                   "９", "０", "~","～", "-", "ー",  ",", "、", "'", "\"", "/", "\\", "・", ";", "；",
                   ":", "：", "<", ">", "＜", "＞", "「", "」", "1", "2", "3", "4", "5", "6", "7",
                   "8", "9", "0", "=", "＝", "?", "？", "."]
    t = Tokenizer()
    tokens = t.tokenize(joined_article_wordlist_before_processed)
    article_wordlist = []
    for token in tokens:
        flag = True
        for ngword in ngwords:
            if ngword in  token.surface:
                flag = False
        if partOfSpeech == '名詞' and flag:
            partOfSpeech = token.part_of_speech.split(',')[0]

            article_wordlist.append(token.surface)
    return article_wordlist

def draw_train_data_from_csv():
    """
     #csvファイルから学習データを読み込み
    """
    #カテゴリごとに収集した学習データが、csvファイルに各記事につき一行という形式で
    # 格納されているので読み込む
    train_data = []
    category_document_number = []
    for i in range(1, 9):
        category_wordlist = []
        with open("category" + str(i) + ".csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                category_wordlist += row
            train_data.append(category_wordlist)
            category_document_number.append(len(category_wordlist))
    #学習データの各カテゴリの記事内で出現した単語のリストを格納したリスト
    #及び、各カテゴリの学習データ内の記事数のリストを返す
    return (train_data, category_document_number)

def calculate_post_prob(train_data, article_wordlist, category_document_number):
    """
    取得URLの記事が各カテゴリに属する事後確率を対数にしたものをリストの形で取得
    """
    log_post_prob_list = []

    for k in range(8):
        #k番目のカテゴリの学習データの単語をキーとしてその出現頻度を格納した辞書を作成
        counter_train_data = col.Counter(train_data[k])
        log_post_prob = 0

        #取得URLの文章の各名詞のカテゴリ内における発生頻度を計算、
        # 各名詞を発生頻度を+1することでゼロ頻度のときの対数関数の発散を防ぐ
        for word in article_wordlist:
            log_post_prob += np.log10((counter_train_data[word] + 1) / (len(train_data[k]) + len(set(train_data[k]))))
        #学習したデータとして利用した全記事内で、
        # k番目のカテゴリの記事の割合を計算、対数に変換して事後確率を対数に変換したものの計算を終了
        log_post_prob += np.log10(category_document_number[k] / sum(category_document_number))
        log_post_prob_list.append(log_post_prob)
    return log_post_prob_list



