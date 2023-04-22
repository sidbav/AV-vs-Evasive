import sys
import os
import subprocess
from pathlib import Path

input_dir = sys.argv[1]
input_dir = Path(input_dir)

output_dir = Path(sys.argv[2])

#print(input_file_path, output_file_path)

for path, subdirs, files in os.walk(input_dir):
	for name in files:
		input_file_path = Path(path, name)
		sample_file_path = Path("Dropper","sample.exe")
		output_file_name = Path(output_dir, name+"_profDropper")
		
		result = subprocess.Popen(["copy", "/Y", input_file_path, sample_file_path], shell=True)

		result.wait()

		result = subprocess.Popen(["rc", Path("Dropper/Resource.rc")], shell=True)

		result.wait()

		result = subprocess.Popen(["cl", "/EHsc", Path("Dropper/*.cpp"), Path("Dropper/Resource.res"), "/link", "/out:"+str(output_file_name)], shell=True)

		#print(result)

		result.wait()

		result = subprocess.Popen(["del", Path("Dropper/Resource.res")], shell=True)

		result.wait()

		result = subprocess.Popen(["del", Path("Dropper/sample.exe")], shell=True)

		result.wait()

		result = subprocess.Popen(["del", Path("Dropper/Source.obj")], shell=True)

		result.wait()







