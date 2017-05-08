# -*- coding: utf-8 -*-
#各カテゴリ100記事(=800記事)について一つ抜き法による精度テストを実施
#分類精度約85.875%

import csv
import collections as col
import numpy as np
from tqdm import tqdm


def NBClassify():

    #csvファイルから学習データを読み込み
    train_data, category_document_number, threed = draw_train_data_from_csv()

    count = 0 #正解数カウント用
    attempt_done = 0 #終了したテスト試行回数カウント用
    attempt = 100 #精度テスト試行回数
    for k in range(8):
        for l in tqdm(range(attempt)):
            train_data_temp = train_data[k]
            for word in threed[k][l]:
                train_data[k].remove(word)


            #取得URLの記事が各カテゴリに属する事後確率を対数にしたものをリストの形で取得
            log_post_prob_list = calculate_post_prob(train_data, threed[k][l], category_document_number)

            #正解であればcount ++
            if k == log_post_prob_list.index(max(log_post_prob_list)):
                count += 1
            attempt_done += 1
            number_to_category = {0: "エンタメ", 1: "スポーツ", 2:"おもしろ", 3:"国内", 4: "海外", 5: "コラム", 6: "IT・科学", 7: "グルメ"}
            #事後確率最大のものを回答として出力
            print("正解:", number_to_category[k], "分類器による分類:", number_to_category[log_post_prob_list.index(max(log_post_prob_list))])
            print("累積正解数:", count, "", "試行回数: " + str(attempt_done) + "/" + str(attempt * 8) + " ", "暫定正解率:", str(count * 100/attempt_done) + "%")
            train_data[k] = train_data_temp
    print("精度テスト終了")
    print("試行回数: " + str(attempt * 8))
    print("精度: " + str(count * 100/(attempt*8)) + "%")





def draw_train_data_from_csv():
    """
     #csvファイルから学習データを読み込み
    """
    #カテゴリごとに収集した学習データが、csvファイルに各記事につき一行という形式で
    # 格納されているので読み込む
    train_data = []
    category_document_number = []
    threed = [[] for n  in range(8)]
    for i in range(1, 9):
        category_wordlist = []
        with open("category" + str(i) + ".csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                threed[i-1].append(row)
                category_wordlist += row
            train_data.append(category_wordlist)
            category_document_number.append(len(category_wordlist))
    #学習データの各カテゴリの記事内で出現した単語のリストを格納したリスト
    #及び、各カテゴリの学習データ内の記事数のリストを返す
    return (train_data, category_document_number, threed)





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
        # 各名詞を発生頻度を+1することでゼロ頻度のときの対数関数の負方向への発散を防ぐ
        for word in article_wordlist:
            log_post_prob += np.log10((counter_train_data[word] + 1) / (len(train_data[k]) + len(set(train_data[k]))))
        #学習したデータとして利用した全記事内で、
        # k番目のカテゴリの記事の割合を計算、対数に変換して足すことで事後確率を対数に変換したものの計算を終了
        log_post_prob += np.log10((category_document_number[k] - 1)/ (sum(category_document_number) - 1))
        log_post_prob_list.append(log_post_prob)
    return log_post_prob_list

if __name__ == '__main__':
    NBClassify()





