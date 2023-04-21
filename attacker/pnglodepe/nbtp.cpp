#include "./lodepng.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>
#include <tuple>
#include <iterator>
#include <Windows.h>

typedef std::vector<unsigned char> DataVect;

void encodeOneStep(const char* filename, std::vector<unsigned char>& image, unsigned width, unsigned height) {
  //Encode the image
  unsigned error = lodepng::encode(filename, image, width, height);

  //if there's an error, display it
  if(error) std::cout << "encoder error " << error << ": "<< lodepng_error_text(error) << std::endl;
}

void encodeTwoSteps(const char* filename, std::vector<unsigned char>& image, unsigned width, unsigned height) {
    std::vector<unsigned char> png;

    // The 8 is key here. Not entirely sure how 8 works theoretically, but it does!
    unsigned error = lodepng::encode(png, image, width, height,LCT_RGB,8);
    if(!error) lodepng::save_file(png, filename);

    //if there's an error, display it
    if(error) std::cout << "encoder error " << error << ": "<< lodepng_error_text(error) << std::endl;
}


DataVect decodeTwoSteps(const char* filename) {
    std::vector<unsigned char> png;
    std::vector<unsigned char> image; //the raw pixels
    unsigned width, height;

    //load and decode
    unsigned error = lodepng::load_file(png, filename);
    if(!error) error = lodepng::decode(image, width, height, png, LCT_RGB, 8);

    //if there's an error, display it
    if(error) std::cout << "decoder error " << error << ": " << lodepng_error_text(error) << std::endl;

    return image;
}

DataVect get_file_bin(const std::string& filename){
    std::ifstream input( filename, std::ios::binary );
    DataVect buffer(std::istreambuf_iterator<char>(input), {});
    return buffer;
}

void write_to_disk(const std::string& filename,const DataVect &data){
    FILE* dest_file = fopen(filename.c_str(),"wb");
    fwrite(&data[0],data.size(),1,dest_file);
    fclose(dest_file);
}

// void raw_image_to_binary(DataVect &input_raw_image){
//     union {uint32_t size;unsigned char bytes[4];} prepend_size_data{};
//     memcpy(prepend_size_data.bytes,&input_raw_image[0],4);

//     //The range used is [first,last), which includes all the elements between first and last, including the element pointed by first but not the element pointed by last.
//     input_raw_image.erase(input_raw_image.begin(),input_raw_image.begin()+4);
//     input_raw_image.erase(input_raw_image.begin() + prepend_size_data.size, input_raw_image.end());
// }


// usage: nbtp b2p/p2b file1 file2
int main(int argc, char** argv){
    if (strcmp(argv[1],"b2p") == 0){
        
        // input binary data output png file
        std::string inputdir = argv[2];
        std::string outputdir = argv[3];
        WIN32_FIND_DATA fileData;
        HANDLE hFind;
        // std::cout << inputdir << outputdir << std::endl;
        hFind = FindFirstFile((inputdir+"\\*.*").c_str(), &fileData);
        if (hFind != INVALID_HANDLE_VALUE) {
            do {
                if (std::string(fileData.cFileName) != "." && std::string(fileData.cFileName) != ".."){
                    DataVect bin = get_file_bin(inputdir + "\\" + fileData.cFileName);
                    std::cout << inputdir + "\\" + fileData.cFileName << std::endl;
                    int size = bin.size();
                    
                    // The 3 comes from the 24 bit RGB values. Each pixel uses 3 bytes of data
                    int area = ceil(float(size)/3.0);

                    // Fixed width and calculating height accordingly
                    int width = 64;
                    int height = ceil(float(area)/float(width));

                    int new_size = width*height*3;
                    std::cout << new_size << std::endl;

                    // Appending additional data to fill out the image dimensions
                    bin.insert(bin.end(),new_size-size, '0');
                    std::string output_filename = outputdir + "\\" + std::string(fileData.cFileName) + ".png";
                    std::cout << output_filename << std::endl;
                    encodeTwoSteps(output_filename.c_str(), bin, width, height);                    
                
                }
            } while (FindNextFile(hFind, &fileData));
            FindClose(hFind);
        } else {
            /* could not find any files in directory */
            std::cerr << "Error: could not find any files in directory." << std::endl;
            return EXIT_FAILURE;
        }
        return EXIT_SUCCESS;


    } else if (strcmp(argv[1],"p2b") == 0){

        DataVect binary_image = decodeTwoSteps(argv[2]);
        write_to_disk(argv[3],binary_image);
    }

}