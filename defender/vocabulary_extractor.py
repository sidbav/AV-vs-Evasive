import json
import os
import sys
import magic

from defender.models.attribute_extractor import *


out_path = ""
train_paths = []

# Parsing out the input files and output file from the command line args
args = sys.argv
input_flag_index = args.index("-i")
output_flag_index = args.index("-o")
train_paths = args[input_flag_index+1:output_flag_index]
out_path = args[output_flag_index+1]

vocab = set()

# The fields that will be used to build the vocab
interesting_fields = ['imports','exports', 'section', 'header', 'optional']
exclude_fields = ['sha256', 'md5', 'appeared', 'label', 'avclass', 'histogram', 'byteentropy']

def travel(element, key_string):
    if type(element) == list:
        for el in element:
            travel(el, key_string)
    elif type(element) == dict:
        for key in element:
            #print(key)
            travel(element[key], key_string+"->"+key)
    elif type(element) == str:
        vocab_element = key_string+"->"+element
#        if vocab_element not in vocab:
#            vocab.append(vocab_element)
        vocab.add(vocab_element)
    elif type(element) == int or type(element) == float:
        pass
    else:
        print(f"Data type not handled at {key_string} with value {element} with type {type(element)}")

#Extracting vocab from a dict of attributes
def dictVocabExtractor(attribs):
    for field_name in attribs.keys():
        if field_name not in exclude_fields: 
            field = attribs[field_name]
            travel(field,field_name)

# Extracting data out of the jsonl train files
def jsonVocabExtractor(file_path):
    with open(file_path,'r') as train_file:
        train_data_list = list(train_file)
    
    file_count = len(train_data_list)
    print(f"File count is {file_count}") 
    for i in range(file_count):
        print(i, end='\r')
        # A percentage progress
        if i == file_count/4: print("25% done")
        elif i == file_count/2: print("50% done")
        elif i == (file_count*3)/4: print("75% done")
        elif i == file_count: print("100% done")
        
        line = train_data_list[i]
        one_file_data = json.loads(line)
        dictVocabExtractor(one_file_data)
        #for field_name in interesting_fields:
#        for field_name in one_file_data.keys():
#            if field_name not in exclude_fields: 
#                field = one_file_data[field_name]
#                travel(field,field_name)

#Extracting vocab out of PE files
def peVocabExtractor(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    extractor = CustomExtractor(file_data)
    attributes = extractor.custom_attribute_extractor()
#    print(type(attributes))
    dictVocabExtractor(attributes)
        

#        print(extractor.custom_attribute_extractor())
        

for train_path in train_paths:
    print(f"Going through the file at {train_path}")

    file_type = magic.from_file(train_path)
    print(file_type)
    if file_type == "JSON data":
        jsonVocabExtractor(train_path)
    elif file_type == "PE32 executable (GUI) Intel 80386, for MS Windows":
        peVocabExtractor(train_path)
    else:
        print("SOME OTHER FILE FOUND ", file_type)


if out_path != "":
    with open(out_path,'w') as file:
        file.write('\n'.join(list(vocab)) + '\n')
else:
    print("Vocab here")
    print(vocab)


