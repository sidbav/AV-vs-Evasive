import sys
import re

input_file = sys.argv[1]

pattern = r'"confidence":(\d+\.\d+),"result":(\d)'
with open(input_file) as file:
    for line in file:
        if line != "\n":
            match = re.search(pattern, line)
            if match:
                confidence = float(match.group(1))
                result = int(match.group(2))

                if result == 1:
                    confidence = 100 - confidence
                    
                print(confidence)
