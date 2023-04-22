/****
 * TO COMPILE: g++ -o output_file -std=c++11 image2binary_CV.cpp  `pkg-config --cflags --libs opencv4`
 * USAGE: ./output_file <input_image> <output_binary_file>
 */

#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

int main(int argc, char** argv) {
    if (argc != 3) {
        cout << "Usage: " << argv[0] << " <input_image> <output_binary_file>" << endl;
        return -1;
    }

    Mat img = imread(argv[1], IMREAD_GRAYSCALE);
    if (img.empty()) {
        cout << "Error: could not read image " << argv[1] << endl;
        return -1;
    }

    ofstream fout(argv[2], ios::out | ios::binary);
    if (!fout) {
        cout << "Error: could not create file " << argv[2] << endl;
        return -1;
    }

    fout.write(reinterpret_cast<const char*>(img.data), img.total() * img.elemSize());
    fout.close();

    return 0;
}

