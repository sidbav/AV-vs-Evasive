# pe_to_npz

## Purpose
Will take an entire directory of either goodware or malware PE folders and will generate the ember features vector for each file in the directory. This will then save the ember feature vector into an output file. This output file (of npz type) file can be loaded in during training of a model

## Usage
```
python pe_to_npz.py <DIRECTORY OF EITHER MALWARE OR GOODWARE FILES> -<b/m> <OUTPUT_FILE_NAME>
```

NOTE: the entire directory should either be GOODWARE (`-b`) OR MALWARE (`-m`)
