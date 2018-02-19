#include <cryptopp/cryptlib.h>
#include <cryptopp/osrng.h> // AutoSeededRandomPool
#include <iostream>
#include <cstdlib>


int main(int, char**) {

    std::cout << "CryptoPP version: " << CRYPTOPP_VERSION << std::endl;

    CryptoPP::AutoSeededRandomPool rng;
    std::cout << "This is a random number from CryptoPP: " << rng.GenerateByte() << std::endl;

    return EXIT_SUCCESS;
}
