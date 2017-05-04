# -*-  coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.shortcuts import render
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer
import csv
import collections as col
import numpy as np

import re



def hello_world(request):
    return HttpResponse('Hello World!')

def hello_template(request):
    #number_of_train_data = {1: 1887, 2: 1982, 3: 1003, 4: 1960, 5: 1939, 6: 1670, 7: 1887, 8: 1619}
    if request.GET.get('your_name'):

        html = urlopen(request.GET.get('your_name'))
        bsobj = BeautifulSoup(html, 'html.parser')
        alist = list(bsobj.findAll(class_="article"))
        b = []
        for i in alist:

            b.append(i.get_text())

        w = "".join(b)

        t = Tokenizer()
        tokens = t.tokenize(w)
        article_wordlist = []
        for token in tokens:

            partOfSpeech = token.part_of_speech.split(',')[0]
            if partOfSpeech == '名詞':
                # print(token.surface)
                article_wordlist.append(token.surface)

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

        whole_train_data = []
        for j in range(len(train_data)):
            print("######")
            whole_train_data += train_data[j]
        counter_whole_train_data = col.Counter(whole_train_data)

        log_post_prob_list = []
        for k in range(8):
            counter_train_data = col.Counter(train_data[k])
            log_post_prob = 0
            for word in article_wordlist:
                log_post_prob += np.log10((counter_train_data[word] + 1)/(len(train_data[k]) + len(set(train_data[k]))))
            log_post_prob += np.log10(category_document_number[k]/sum(category_document_number))
            log_post_prob_list.append(log_post_prob)



        number_to_category = {0: "エンタメ", 1: "スポーツ", 2:"おもしろ", 3:"国内", 4: "海外", 5: "コラム", 6: "IT・科学", 7: "グルメ"}
        d = {

            'message': number_to_category[log_post_prob_list.index(max(log_post_prob_list))]  #number_to_category[log_count_list.index(max(log_count_list))]
        }
        return render((request), 'index.html', d)
    else:
        return render(request, 'index.html', {'hour': "", 'message': ""})

def hello_get_query(request):

    if request.GET.get('your_name'):
        d = {
            'your_name': int(request.GET.get('your_name')) ** 10
        }
        return render(request, 'get_query.html', d)
    else:
        return render(request, 'get_query.html', {'your_name': ""})