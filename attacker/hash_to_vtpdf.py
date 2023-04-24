from pyhtml2pdf import converter
import sys
import requests
from pathlib import Path
import time
import random

sha256_hash_file = sys.argv[1]
output_dir = sys.argv[2]

count = 0
with open(sha256_hash_file, 'r') as f:
    for line in f:
        count += 1
        sha256, file_name = line.split()
        file_name = file_name.split('/')[1]
        #print(file_name, sha256)

        output_pdf_file = Path(output_dir, file_name+'_behavior.pdf')
        vt_link_behavior = f'https://www.virustotal.com/gui/file/{sha256}/behavior'

        converter.convert(vt_link_behavior, output_pdf_file)
        print(output_pdf_file)
        ## So VirusTotal doesnt think you are a robot/script LOL
        if count % 10 == 0:
            print('****************************sleeping 15 seconds, check how the pdfs are doing')
            time.sleep(15)

