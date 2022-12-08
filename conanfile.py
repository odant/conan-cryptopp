from conans import ConanFile, CMake, tools
import os

class CryptoppConan(ConanFile):
    name = "cryptopp"
    version = "8.7.0+0"
    license = "Boost Software License 1.0 - https://raw.githubusercontent.com/weidai11/cryptopp/master/License.txt"
    description = "Crypto++: free C++ Class Library of Cryptographic Schemes"
    url = "https://github.com/odant/conan-cryptopp"
    settings = {
        "os": ["Windows", "Linux"],
        "compiler": ["Visual Studio", "gcc"],
        "build_type": ["Debug", "Release"],
        "arch": ["x86_64", "x86", "mips", "armv7"]
    }
    options = {
        "ninja": [True, False]
    }
    default_options = {
        "ninja": True
    }    
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt", "FindCryptoPP.cmake", "cmake.patch", "allow_clang-cl.patch"
    no_copy_source = True
    build_policy = "missing"

    def isClangClToolset(self):
        return True if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio" and str(self.settings.compiler.toolset).lower() == "clangcl" else False
    
    def configure(self):
        toolset = str(self.settings.compiler.get_safe("toolset"))
        if toolset.endswith("_xp"):
            raise Exception("This package is not compatible Windows XP")
        # Only C++11
        if self.settings.compiler.get_safe("libcxx") == "libstdc++":
            raise Exception("This package is only compatible with libstdc++11")
        if self.isClangClToolset():
            self.options.ninja = False

    def build_requirements(self):
        if self.options.ninja:
            self.build_requires("ninja/[>=1.10.2]")
            
    def source(self):
        tools.patch(patch_file="cmake.patch")
        #if self.settings.os == "Windows":
        #    tools.patch(patch_file="allow_clang-cl.patch")
        
    def build(self):
        cmakeGenerator = "Ninja" if self.options.ninja else None
        cmake = CMake(self, generator=cmakeGenerator)
        cmake.definitions["CRYPTOPP_SOURCES"] = os.path.join(self.source_folder, "src")
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
        self.copy("*cryptopp*.lib", dst="lib", keep_path=False)
        self.copy("*cryptopp.pdb", dst="bin", keep_path=False)

    def package_id(self):
        self.info.options.ninja = "any"

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
