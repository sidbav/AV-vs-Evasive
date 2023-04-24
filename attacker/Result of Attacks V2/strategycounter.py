import re
import pandas as pd
import numpy as np

strategy =dict()
        
strategy['S1'] = "evade_addedfunc1"
strategy['S2'] = "evade_img_withgdi_addedfunc2"
strategy['S3'] = "evade_noimg_addedfunc"
strategy['S4'] = "evade_noimg_addedfunc_withgdi32"
strategy['S5'] = "evade_noimg_withgdi_addedfunc2"

#models = ["amit","lidsu","ourModel","vicente","yasirModel","yasirPipe"]
models = ["amit","lidsu","ourModel","vicente","yasirModel"]

data = {
        "S1":np.zeros(50,dtype=np.int8),
        "S2":np.zeros(50,dtype=np.int8),
        "S3":np.zeros(50,dtype=np.int8),
        "S4":np.zeros(50,dtype=np.int8),
        "S5":np.zeros(50,dtype=np.int8),
        }
df = pd.DataFrame(data)

for s in ["S1","S2","S3","S4","S5"]:
    for m in models:
        fileName = f"./{strategy[s]}_results/{strategy[s]}_{m}.txt"
        with open(fileName) as file:
            for count, line in enumerate(file):
                if count == 00 or count%2 == 0 or line == "" or line == " ": 
                    continue
                pattern = r'"result":(\d+)'
                match = re.search(pattern,line)
                if match != None:
                    result = int(match.group(1))
                    if result == 0:
                        df[s][(count-1)/2] += 1.0

print(df)

for i in range(50):
    success = ""

    for s in ["S1","S2","S3","S4","S5"]:
        if df[s][i] == 5:
            success += f"{s} "

    print(f"{i} - {success}")

    
