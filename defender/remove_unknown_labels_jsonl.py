import json
import sys
import os

def usage():
  print("Usage: python remove_unknown_labels_jsonl.py <JSONL FILE>")
  print()
  sys.exit()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()

    arg = sys.argv[1]
    if not os.path.isfile(arg):
        print(f'{arg} does not exist')
        usage()

    if arg[-5::] != 'jsonl':
        print(f'{arg} is not a jsonl file!')
        usage()

    jsonl_file_path = os.path.abspath(arg)

    total = 0
    unknown = 0
    left = 0
    new_full_file_path = jsonl_file_path + 'UNKNOWN_REMOVED'

    print('processing', jsonl_file_path)

    with open(jsonl_file_path, 'r') as json_file:
        json_list = list(json_file)

    total = len(json_list)
    updated_json_list = []
    for json_str in json_list:
        json_obj = json.loads(json_str)
        if json_obj['label'] != -1:
            updated_json_list.append(json_obj)
            left += 1
        else:
            unknown += 1
    
    print('writing to new file now')
    with open(new_full_file_path, 'w') as updated_json_file:
        for json_obj in updated_json_list:
            json.dump(json_obj, updated_json_file)
            updated_json_file.write('\n')


    print('total, unknown, left', total, unknown, left)
    print('done with', jsonl_file_path, 'created', new_full_file_path)

