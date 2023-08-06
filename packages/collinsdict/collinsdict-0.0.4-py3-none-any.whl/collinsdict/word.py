import requests
import re
import sqlite3
from bs4 import BeautifulSoup

from .db import DB

URL = 'http://dict.youdao.com/w/'

class Word():
    '''Word'''
    def __init__(self,word):
        self.word = word
        self.phonetic = ''
        self.star = None
        self.rank = None
        self.trans = []
        self.addition = ''
        self.db = DB()
        self.getDatas()

    def getDatas(self):
        # self.fromWeb()
        try:
            result = self.db.get(self.word)
            self.phonetic = result['Phonetic']
            self.rank = result['Rank']
            self.star = result['Star']
            self.addition = result['Addition']
            self.trans = result['Trans']
        except Exception as err:
            print(err)
            self.fromWeb()

    def fromWeb(self):
        print("Get data from web")
        r = requests.get(URL+self.word)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text,'lxml')
        # Get collins result
        collinstext = soup.find("div",id="collinsResult")
        # Meta data
        for i in collinstext.h4.find_all():
            if "spell" in i['class']:
                self.phonetic = i.string
            elif "star" in i['class']:
                self.star = i['class'][-1][-1]
            elif "rank" in i['class']:
                self.rank = i.string
            elif "additional" in i['class']:
                if 'also' not in i.string:
                    self.addition += re.sub('[ \t\n]','',i.string)+';'
                else:
                    self.addition += i.string+';'
        # Translations
        trans = collinstext.ul
        for i in trans.find_all('li'):
            major = i.find('div','collinsMajorTrans')
            order = major.span.string[:-2]
            major = '  '.join([i.strip() for i in major.get_text().split('\n') if i][1:])
            examples = i.find_all('div','exampleLists')
            examples = [''.join(x.get_text().split('\n')) for x in examples]
            self.trans.append({
                'Order' : order,
                'Major' : major,
                'Examples' : examples
            })
        print('Insert into DB')
        result = {
            'Word' : self.word,
            'Phonetic' : self.phonetic,
            'Rank' : self.rank,
            'Star' : self.star,
            'Addition' : self.addition,
            'Trans' : self.trans
        }
        self.db.insert(result)
        return result

    def __str__(self):
        text = "Word    : "+self.word+'\n'
        text += "Phonetic: "+self.phonetic+'\n'
        text += "Star    : "+self.star+'\n'
        text += "Rank    : "+self.rank+'\n'
        text += "Addition: "+self.addition+'\n'
        # Translations
        text += "Translations:\n"
        for i in self.trans:
            text += '      '+i['Order']+' : '+i['Major']+'\n'
            for j in i['Examples']:
                text += '    '+j+'\n'
        return text
