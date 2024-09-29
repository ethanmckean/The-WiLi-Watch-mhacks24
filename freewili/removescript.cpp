// #include <iostream>
// #include <fstream>
// #include <string>
// #include <sstream>
// #include <vector>

// std::vector<int> parseSubFile(const std::string &filename) {
//     std::ifstream infile(filename);
//     std::vector<int> rawData;
//     std::string line;

//     while (std::getline(infile, line)) {
//         if (line.find("RAW_Data:") != std::string::npos) {
//             size_t pos = line.find(":") + 1;
//             std::string dataStr = line.substr(pos);
//             std::istringstream iss(dataStr);
//             int num;
//             while (iss >> num) {
//                 rawData.push_back(num);
//             }
//         }
//     }
//     return rawData;
// }

// extern "C" {
//     void processRawData(const int *data, size_t size) {
//         // Your processing logic here
//     }
// }

// int main() {
//     auto data = parseSubFile("white.sub");
//     processRawData(data.data(), data.size());
//     return 0;
// }

#include "fwwasm.h"
// Send IR Data
int main()
{
    removeFileOrDirectory("/scripts/subtitle_processor.wasm");
    return 0;
}