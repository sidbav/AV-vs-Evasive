import sys
import re

args = sys.argv

file_path_1 = args[1]
file_path_2 = args[2]


vocab1_set = set()
vocab1_count = dict()

vocab2_set = set()
vocab2_count = dict()

with open(file_path_1) as file_1:
    for line in file_1:
        #print(line)
        regex_result = re.match("^(.*) = (.*)$", line)
        if regex_result != None:
            vocab_word = regex_result.groups()[0]
            vocab_word_count = regex_result.groups()[1]
            vocab1_set.add(vocab_word)
            vocab1_count[vocab_word] = vocab_word_count
        else:
            print(line)


with open(file_path_2) as file_2:
    for line in file_2:
        regex_result = re.match("^(.*) = (.*)$", line)
        if regex_result != None:
            vocab_word = regex_result.groups()[0]
            vocab_word_count = regex_result.groups()[1]
            vocab2_set.add(vocab_word)
            vocab2_count[vocab_word] = vocab_word_count
        else:
            print(line)
            break
        #regex_result = re.match("^(.*) = (.*)$", line)
        #vocab_word = regex_result.groups()[0]
        #vocab_word_count = regex_result.groups()[1]
        #vocab2_set.add(vocab_word)
        #vocab2_count[vocab_word] = vocab_word_count

#vocab1 = set(re.sub(" = .*$", '', line).strip() for line in open(file_path_1))
#vocab2 = set(re.sub(" = .*$", '', line).strip() for line in open(file_path_2))
#
#new_words = vocab1_set.difference(vocab2_set)
##print(new_words)
##print("\n".join(new_words))
#
#for word in new_words:
#    print(f"{word} = {vocab1_count[word]}")
#
