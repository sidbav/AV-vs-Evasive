import cv2
import numpy as np
import sys
import os.path

# Check if correct number of command line arguments were provided
if len(sys.argv) != 3:
    print("Usage: python binary2image_CV.py input_file output_file")
    sys.exit()

# Get input and output file names from command line arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# Check if input file exists
if not os.path.exists(input_file):
    print("Input file does not exist")
    sys.exit()

# Read binary data from the input file
with open(input_file, "rb") as f:
    binary_data = f.read()

# Convert binary data to NumPy array
image_data = np.frombuffer(binary_data, dtype=np.uint8)

# Reshape the array into a 2D array with the desired size (e.g. 200x200)
#image_data = image_data.reshape((200, 200))
data_size = len(image_data) 

width = 1024
height = data_size/width
real_bytes = int((height - int(height))*width)
height = int(height)
remaining_bytes_to_add = width - real_bytes
print('bytes to add', remaining_bytes_to_add);

if remaining_bytes_to_add != 0:
    height += 1
    arr_bytes = np.array([0]*remaining_bytes_to_add)
    image_data = np.append(image_data, arr_bytes)

print(height, width)
image_data = image_data.reshape((height, width))

# Write the image data to a file
cv2.imwrite(output_file, image_data)

print("Image written to", output_file)

