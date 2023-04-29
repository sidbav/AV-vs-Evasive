# script to pack files

import subprocess
import sys 
import os 

#this just helps to call the fucntion directly in the terminal
def usage():
  print("Usage: python pack_files.py <DIRECTORY_OF_EITHER_MALWARE_OR_GOODWARE_FILES> <OUTPUT_FILE_DIRECTORY>")
  print("Pass in either an either Malware folder OR Goodware Folder")
  print()
  sys.exit()

# pack files using upx 
def pack_upx(unpackedDirectory, packedDirectory):
	for path, subdirs, files in os.walk(unpackedDirectory):
	    for name in files:
	      file_name = os.path.join(path, name)
	      packed_name = name + "_upx" #create upx name
	      file_path = os.path.join(packedDirectory, packed_name)
	      subprocess.call(["upx", file_name, "-o", file_path])


if __name__ == "__main__":

	#subprocess.call(["ls", "-l"])
	#sys.exit()


	if len(sys.argv) != 3:
		usage()

	unpackedDirectory = sys.argv[1] #input
	packedDirectory = sys.argv[2] #output

	pack_upx(unpackedDirectory, packedDirectory)
