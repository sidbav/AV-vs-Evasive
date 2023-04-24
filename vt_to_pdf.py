from pyhtml2pdf import converter
import sys
import requests
from pathlib import Path

sha256_hash_file = sys.argv[1]
output_dir = sys.argv[2]

with open(sha256_hash_file, 'r') as f:
    for line in f:
        sha256, file_name = line.split()
        file_name = file_name.split('/')[1]
        #print(file_name, sha256)

        output_pdf_file = Path(output_dir, file_name+'_behavior.pdf')
        vt_link_behavior = f'https://www.virustotal.com/gui/file/{sha256}/behavior'

        converter.convert(vt_link_behavior, output_pdf_file)
        print(output_pdf_file)
