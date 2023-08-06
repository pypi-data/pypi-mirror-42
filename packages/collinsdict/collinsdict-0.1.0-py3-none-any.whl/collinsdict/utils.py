import time
import os
from .word import Word

home = os.path.dirname(__file__)
def autoGet(wordsFile=home+'/temp/wordsList.txt'):
    ftmp = open(home+'/temp/ableList.txt','a')
    with open(wordsFile,'r+') as f:
        line = f.readline()
        while(line):
            word = Word(line.strip())
            if word.flag == 1:
                ftmp.write(line)
                time.sleep(2)
            line = f.readline()
    ftmp.close()


    print("Auto get complete")
