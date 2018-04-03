project(PackageTest CXX)
cmake_minimum_required(VERSION 3.0)

include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(CryptoPP REQUIRED)

enable_testing()

add_executable(test_package test_package.cpp)
target_link_libraries(test_package CryptoPP::CryptoPP)
set_target_properties(test_package
    PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH True
)
add_test(
    NAME test_package
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin
    COMMAND test_package
)

add_executable(test_package_CONAN_PKG test_package.cpp)
target_link_libraries(test_package_CONAN_PKG CONAN_PKG::cryptopp)
set_target_properties(test_package_CONAN_PKG
    PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH True
)
add_test(
    NAME test_package_CONAN_PKG
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin
    COMMAND test_package_CONAN_PKG
)
