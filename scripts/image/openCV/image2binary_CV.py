import cv2
import argparse

# Set up the command line arguments
parser = argparse.ArgumentParser(description='Convert image to bytes.')
parser.add_argument('input_file', type=str, help='path to input file')
parser.add_argument('output_file', type=str, help='path to output file')

# Parse the command line arguments
args = parser.parse_args()

# Read the input image
input_image = cv2.imread(args.input_file, cv2.IMREAD_GRAYSCALE)

# Convert the image to bytes
bytes_data = input_image.tobytes()

# Write the bytes data to the output file
with open(args.output_file, 'wb') as output_file:
    output_file.write(bytes_data)

