import os
import subprocess
import requests
import json
import numpy as np

URL = "http://127.0.0.1:8080/"

import sys

if len(sys.argv) != 2:
    print("Usage: python test_dir.py <DIR_OF_FILES>")
    sys.exit(1)

directory_path = sys.argv[1]

if not os.path.isdir(directory_path):
    print("Usage: python test_dir.py <DIR_OF_FILES>")
    sys.exit(1)


classified_malware = 0
classified_goodware = 0
non_200_status_files_malware_files = []
num_files = 0

print("startin to process",directory_path)
for path, subdirs, files in os.walk(directory_path):
    for name in files:
        file_name = os.path.join(path, name)
        with open(file_name, 'rb') as file:
            data = file.read()
            res = requests.post(url=URL, data=data, headers={'Content-Type': 'application/octet-stream'})
            num_files+=1
            print(num_files, file_name, res.text)
            if res.status_code == 200:
                result = json.loads(res.text)["result"]
                if result == 1:
                    classified_malware += 1
                elif result == 0:
                    classified_goodware += 1


print('NUM MALWARE', classified_malware)
print('NUM GOODWARE', classified_goodware)
