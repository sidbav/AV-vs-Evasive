import json
import os

def rec_print(my_dict, prefix=""):        
    for key in list(my_dict.keys()):
        # print(prefix)
        print(prefix + key, end=" ")
        key_type = type(my_dict[key])
        if key_type != dict:
            print(key_type)
        else:
            print("")
        if type(my_dict[key]) == dict:
            rec_print(my_dict[key],prefix+"\t")

data_dir = "./"
raw_feature_paths = [os.path.join(data_dir, "train_features_{}.jsonl".format(i)) for i in range(6)]

# sample_count = 0
# for feature_path in raw_feature_paths:
#     with open(feature_path,'r') as train_file:
#         train_list = list(train_file)
#         sample_count += len(train_list)

# print(sample_count)
with open('./train_features_0.jsonl','r') as train_file:
    train_list = list(train_file)

train_entry = json.loads(train_list[0])
# print(train_entry.keys()[0])


rec_print(train_entry)

# print(len(train_list))