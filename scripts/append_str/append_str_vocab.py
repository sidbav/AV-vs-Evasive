import os 
import sys
import random

goodware_vocab = sys.argv[1]
filename = sys.argv[2]

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

with open(filename, 'r+b') as f:
    f.seek(0, 2)
    f.write(appended_str)

print(f'{filename} modified.')
