# nbtp.cpp

## Purpose
Source code for a tool derived from https://gist.github.com/Neboer/f47a7fa2006650e9350a384225f94a4f that converts binary to png files and png files to binary using the image manipulation library lodepng. The tool should be compiled and would require lodepng.cpp and lodepng.h to exist in the same directory as lodepng.cpp

The tool takes in a directory of input files, converts it and output it into a directory(should already exist)

## Usage
```
Convert a directory of binary files into png files:
nbtp.exe -b2p <INPUT_DIR> <OUTPUT_DIR>

Convert a directory of png files into binary files:
nbtp.exe -p2b <INPUT_DIR> <OUTPUT_DIR>
```
