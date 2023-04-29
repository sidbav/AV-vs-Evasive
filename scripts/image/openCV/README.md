# binary2image_CV.py

## Purpose
Takes as input a binary file (exe) and convert it to an image using openCV

## Usage
```
python binary2image_CV.py input_file.exe output_file.png
```

# image2binaryCV.cpp

## Purpose
Takes an image file and converts it to a binary file

## Usage
Compiling (Linux)
```
g++ -o img2bin -std=c++11 image2binary_CV.cpp  `pkg-config --cflags --libs opencv4`
```
Running:
```
./img2bin <inputimage> <output_binary_file>
```

# image2binary_CV.py

## Purpose
Takes an image file and converts it to a binary file

## Usage
```
python image2binary_CV.py <inputimage> <output_binary_file>
```
