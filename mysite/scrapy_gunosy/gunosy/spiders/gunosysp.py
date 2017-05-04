# -*- coding: utf-8 -*-
import scrapy
from gunosy.items import GunosyItem
from janome.tokenizer import Tokenizer
import csv
class GunosyspSpider(scrapy.Spider):
    name = "gunosysp"
    allowed_domains = ["gunosy.com"]
    start_urls = ['https://gunosy.com/categories/1',
                        'https://gunosy.com/categories/2',
                        'https://gunosy.com/categories/3',
                        'https://gunosy.com/categories/4',
                        'https://gunosy.com/categories/5',
                        'https://gunosy.com/categories/6',
                        'https://gunosy.com/categories/7',
                        'https://gunosy.com/categories/8']




    def parse(self, response):

        for article in response.css("div.list_title a::attr(href)").extract():
            print(article, "########")
            request = scrapy.Request(response.urljoin(article), callback=self.parse_article)
            request.meta["category"] = int(response.url.split("/")[4][0])
            yield request
        yield scrapy.Request(response.urljoin(response.css("div.pager-link-option a::attr(href)").extract_first()), callback=self.parse)

    def parse_article(self, response):
        ngwords = ["(", ")", "（", "）", "[", "]", "１", "２", "３", "４", "５", "６", "７", "８",
                   "９", "０", "~","～", "-", "ー",  ",", "、", "'", "\"", "/", "\\", "・", ";" "；",
                   ":", "：", "<", ">", "＜", "＞", "「", "」", "1", "2", "3", "4", "5", "6", "7",
                   "8", "9", "0", "=", "?", "？"]
        t = Tokenizer()
        wordlist = []
        category = response.meta["category"]


        tokens = t.tokenize("".join(response.css("div.article p::text").extract()))
        for token in tokens:
            flag = True
            partOfSpeech = token.part_of_speech.split(',')[0]
            if partOfSpeech == '名詞':
                for ngword in ngwords:
                    if ngword  in token.surface:
                        flag = False
                if flag:
                    wordlist.append(token.surface)



        with open('category' + str(category) + '.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(wordlist)
        """
        for sentence in response.css("div.article p::text").extract():
            print(sentence)

        """
