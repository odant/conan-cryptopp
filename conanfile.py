from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


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
    #generators = "cmake"
    exports_sources = "src/*"
    no_copy_source = False # Build in source
    build_policy = "missing"

    def configure(self):
        # Only C++11
        if "libcxx" in self.settings.compiler.fields:
            if self.settings.compiler.libcxx == "libstdc++":
                raise Exception("This package is only compatible with libstdc++11")

    def requirements(self):
        pass
        #self.requires("zlib/[~=1.2.11]@%s/stable" % self.user)
        #self.requires("openssl/[~=1.1.0g]@%s/testing" % self.user)
        #self.requires("boost/1.66.0@%s/testing" % self.user)

    def build(self):
        if self.settings.os == "Windows":
            pass
        else:
            self.build_unix()
        
    def build_unix(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = True
        env_vars = env_build.vars
        env_vars["VERBOSE"] = "1"
        with tools.environment_append(env_vars), tools.chdir(os.path.join(self.source_folder, "src")):
            self.run("env")
            self.run("make -j%s static" % tools.cpu_count())

    def package(self):
        self.copy("*.h", dst="include/cryptopp", keep_path=True)
        self.copy("*.a", dst="lib")
        self.copy("*.lib", dst="lib")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        #self.cpp_info.defines = ["PION_STATIC_LINKING"]
