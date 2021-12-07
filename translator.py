import json

import requests
from bs4 import BeautifulSoup
from word import Word

class Translater:
    def __init__(self):
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch", "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
            "Cache-Control": "max-age=0",
        })
        self.word = None

    def get_cambridge(self, word_str):
        try:
            self.word = Word()
            self.word.text = word_str
            r = self.s.get("http://www.iciba.com/%s" % word_str)
            pass
        except Exception as e:
            print(e)


    def get(self, word_str):
        try:
            self.word = Word()
            self.word.text = word_str
            r = self.s.get("http://www.iciba.com/%s" % word_str)
            soup = BeautifulSoup(r.content, "lxml")
            temp_results = soup.find_all("div", class_="FoldBox_fold__1GZ_2")
            if not temp_results:
                return True
            base = temp_results[0]
            #print(base)
            # 获取基本词义
            temp_results = base.find_all('ul', class_='Mean_part__1Xi6p')
            if temp_results:
                # print(temp_results)
                temp = temp_results[0]
                for node in temp:
                    if len(node.contents) != 2:
                        self.word.props[''] = node.text
                    else:
                        temp_prop = node.contents[0].text
                        # print(temp_prop)
                        temp_str = node.contents[1].text
                        self.word.props[temp_prop] = temp_str
            # 获取句子翻译
            temp_results_sentence = base.find_all(class_='Mean_definition__3yuL7')
            if temp_results_sentence:
                base = temp_results_sentence[0]
                temp_p = base.find_all('p')
                # print(temp_p[0].text)
                self.word.props[''] = temp_p[0].text
        except Exception as e:
            print(e)

if __name__ == '__main__':
    a=Translater()
    a.get("dataChanged")
    print(a.word.props)
    a.get("Please enter the characters you see in the image below into the text box provided.")
    print(a.word.props)
