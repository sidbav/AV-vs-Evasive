import os 
import sys
import random

goodware_vocab = sys.argv[1]
filename = sys.argv[2]

"""
def read_file(goodware_vocab):
    results = []
    with open(goodware_vocab, 'r') as f:
        line = f.readline().strip()
        parts = line.split('->')
        string = parts[-1].split(' ')[0]
        results.append(string)

    random.shuffle(results)

    appended_str = ' '.join(results)
    return appended_str

appended_str = read_file(goodware_vocab)
appended_str = bytes(appended_str, 'utf-8')
"""
appended_str = 'a;sldkfja;lksdjf;lkasjdf;lkjasd;lfjaq;ekrht[\'             opiqnsvdc;w              oijf;lakshjdf;liaht5h2wo \
                        ;idfnvpoiqn 23 ropu8navd                        c                    pfon42-]0g9hjfneqw \'pawifas;d                        asdf     qwer    2i34nasdf;l iehjwf;liand fsoeirtw j`2c4t3gbnf0-x `xwqdsvc-=,o\w dc;kvnhjzm'*45

appended_str = bytes(appended_str, 'utf-8')

with open(filename, 'r+b') as f:
    f.seek(0, 2)
    f.write(appended_str)

print(f'{filename} modified.')
