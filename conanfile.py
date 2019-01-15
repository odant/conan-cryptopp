from conans import ConanFile, tools


class CryptoppConan(ConanFile):
    name = "cryptopp"
    version = "8.0.0+0"
    license = "Boost Software License 1.0 - https://raw.githubusercontent.com/weidai11/cryptopp/master/License.txt"
    description = "Crypto++: free C++ Class Library of Cryptographic Schemes"
    url = "https://github.com/odant/conan-cryptopp"
    settings = {
        "os": ["Windows", "Linux"],
        "compiler": ["Visual Studio", "gcc"],
        "build_type": ["Debug", "Release"],
        "arch": ["x86_64", "x86", "mips"]
    }
    options = {
        "with_unit_tests": [False, True]
    }
    default_options = "with_unit_tests=False"
    generators = "cmake"
    exports_sources = "src/*", "FindCryptoPP.cmake"
    no_copy_source = False
    build_policy = "missing"

    def configure(self):
        toolset = str(self.settings.compiler.get_safe("toolset"))
        if toolset.endswith("_xp"):
            raise Exception("This package is not compatible Windows XP")
        # Only C++11
        if self.settings.compiler.get_safe("libcxx") == "libstdc++":
            raise Exception("This package is only compatible with libstdc++11")

    def build(self):
        if self.settings.os == "Windows":
            self.build_msvc()
        else:
            self.build_unix()

    def build_msvc(self):
        pass

    def build_unix(self):
        cxx_flags = [
            "-std=c++11",
            "-fPIC"
        ]
        if self.settings.arch == "x86":
            cxx_flags.append("-m32")
        elif self.settings.arch == "x86_64":
            cxx_flags.append("-m64")
        if self.settings.build_type == "Release":
            cxx_flags.extend([
            "-DNDEBUG",
            "-g2",
            "-O3"
            ])
        else:
            cxx_flags.extend([
            "-g3",
            "-O0"
            ])
        env = {
            "CXXFLAGS": " ".join(cxx_flags),
            "PREFIX": self.package_folder
        }
        with tools.environment_append(env), tools.chdir("src"):
            self.run("make static -j %s" % tools.cpu_count())
            if self.options.with_unit_tests:
                self.run("make cryptest.exe -j %s" % tools.cpu_count())
                self.run("make test")

    def package(self):
        self.copy("FindCryptoPP.cmake", src=".", dst=".")
        self.copy("*.h", src="src", dst="include/cryptopp", keep_path=True)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*cryptopp-static.lib", dst="lib", keep_path=False)
        self.copy("*cryptopp-object.pdb", dst="bin", keep_path=False)

    def package_id(self):
        self.info.options.with_unit_tests = "any"

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

