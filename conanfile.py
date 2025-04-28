from conan import ConanFile, tools
import os

class CryptoppConan(ConanFile):
    name = "cryptopp"
    version = "8.9.0+0"
    license = "Boost Software License 1.0 - https://raw.githubusercontent.com/weidai11/cryptopp/master/License.txt"
    description = "Crypto++: free C++ Class Library of Cryptographic Schemes"
    url = "https://github.com/odant/conan-cryptopp"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "fPIC": [True, False],
        "ninja": [True, False]
    }
    default_options = {
        "fPIC": True,
        "ninja": True
    }    
    exports_sources = "src/*", "cmake.patch", "allow_clang-cl.patch"
    no_copy_source = True
    build_policy = "missing"
    package_type = "static-library"
    
    def layout(self):
        tools.cmake.cmake_layout(self, src_folder="src");

    def isClangClToolset(self):
        return True if self.settings.os == "Windows" and self.settings.compiler == "msvc" and str(self.settings.compiler.toolset).lower() == "clangcl" else False
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            
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
            self.build_requires("ninja/[>=1.12.1]")
            
    def source(self):
        tools.files.patch(self, patch_file="cmake.patch")
        #if self.settings.os == "Windows":
        #    tools.patch(patch_file="allow_clang-cl.patch")
        
    def generate(self):
        benv = tools.env.VirtualBuildEnv(self)
        benv.generate()
        renv = tools.env.VirtualRunEnv(self)
        renv.generate()
        if tools.microsoft.is_msvc(self):
            vc = tools.microsoft.VCVars(self)
            vc.generate()
        cmakeGenerator = "Ninja" if self.options.ninja else None
        tc = tools.cmake.CMakeToolchain(self, generator=cmakeGenerator)
        tc.variables["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.get_safe("fPIC", True)
        tc.variables["BUILD_STATIC"] = "ON"
        tc.variables["BUILD_SHARED"] = "OFF"
        tc.variables["BUILD_TESTING"] = "OFF"
        tc.generate()
        
    def build(self):
        cmake = tools.cmake.CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        tools.files.copy(self, "*.h", src=self.source_folder, dst=os.path.join(self.package_folder, "include/cryptopp"), keep_path=True)
        tools.files.copy(self, "*.a", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        tools.files.copy(self, "*cryptopp*.lib", src=self.build_folder, dst=os.path.join(self.package_folder, "lib"), keep_path=False)
        tools.files.copy(self, "*cryptopp.pdb", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"), keep_path=False)

    def package_id(self):
        self.info.options.ninja = "any"

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "CryptoPP")
        self.cpp_info.set_property("cmake_target_name", "CryptoPP::CryptoPP")
        self.cpp_info.libs = tools.files.collect_libs(self)
