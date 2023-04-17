import sys
import os
import subprocess
from pathlib import Path

input_file_path = sys.argv[1]
input_file_path = Path(input_file_path,"")
output_file_path = Path(".\Dropper","sample.exe")

print(input_file_path, output_file_path)

#result = subprocess.Popen([Path("C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build/vcvars64.bat")], shell=True)

#result.wait()

#result = subprocess.Popen(["cl"], shell=True)

result = subprocess.Popen(["copy", input_file_path, output_file_path], shell=True)

result.wait()

result = subprocess.Popen(["rc", Path("Dropper/Resource.rc")], shell=True)

result.wait()

result = subprocess.Popen(["cl", "/EHsc", Path("Dropper/*.cpp"), Path("Dropper/Resource.res"), "/link", "/out:MyProgram.exe"], shell=True)

print(result)

