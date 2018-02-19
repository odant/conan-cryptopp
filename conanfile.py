from conans import ConanFile, CMake, tools


class CryptoppConan(ConanFile):
    name = "cryptopp"
    version = "5.6.5"
    license = "Boost Software License 1.0 - https://raw.githubusercontent.com/weidai11/cryptopp/master/License.txt"
    description = "Crypto++: free C++ Class Library of Cryptographic Schemes"
    url = "https://github.com/odant/conan-cryptopp"
    settings = {
        "os": ["Windows", "Linux"],
        "compiler": ["Visual Studio", "gcc"],
        "build_type": ["Debug", "Release"],
        "arch": ["x86_64", "x86"]
    }
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt", "FindCryptoPP.cmake"
    no_copy_source = True
    build_policy = "missing"

    def configure(self):
        # Only C++11
        if "libcxx" in self.settings.compiler.fields:
            if self.settings.compiler.libcxx == "libstdc++":
                raise Exception("This package is only compatible with libstdc++11")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE:BOOL"] = "ON"
        cmake.definitions["BUILD_STATIC:BOOL"] = "ON"
        cmake.definitions["BUILD_SHARED:BOOL"] = "OFF"
        cmake.definitions["BUILD_TESTING:BOOL"] = "OFF"
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("FindCryptoPP.cmake", src=".", dst=".")
        self.copy("*.h", src="src", dst="include/cryptopp", keep_path=True)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*cryptopp-static.lib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
