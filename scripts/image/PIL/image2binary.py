import argparse
from PIL import Image


if __name__ == "__main__":
    # Set up the command line arguments
    parser = argparse.ArgumentParser(description='Convert image to bytes (exe).')
    parser.add_argument('input_file', type=str, help='path to input file')
    parser.add_argument('output_file', type=str, help='path to output file')

    # Parse the command line arguments
    args = parser.parse_args()

    # Open the input image
    input_image = Image.open(args.input_file)

    # Get the uncompressed pixel data
    pixel_data = input_image.getdata()

    # Convert the pixel data to bytes
    bytes_data = bytes(pixel_data)
    print(len(bytes_data))

    # Write the bytes data to the output file
    with open(args.output_file, "wb") as output_file:
        output_file.write(bytes_data)
