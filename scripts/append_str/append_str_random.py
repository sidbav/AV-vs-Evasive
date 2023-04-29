import os 
import sys
import random

filename = sys.argv[1]

appended_str = 'a;sldkfja;lksdjf;lkasjdf;lkjasd;lfjaq;ekrht[\'             opiqnsvdc;w              oijf;lakshjdf;liaht5h2wo \
                        ;idfnvpoiqn 23 ropu8navd                        c                    pfon42-]0g9hjfneqw \'pawifas;d                        asdf     qwer    2i34nasdf;l iehjwf;liand fsoeirtw j`2c4t3gbnf0-x `xwqdsvc-=,o\w dc;kvnhjzm'*45

appended_str = bytes(appended_str, 'utf-8')

with open(filename, 'r+b') as f:
    f.seek(0, 2)
    f.write(appended_str)

print(f'{filename} modified.')
