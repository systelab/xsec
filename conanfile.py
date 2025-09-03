from conan import ConanFile
from conan.tools.files import copy, collect_libs
from conan.tools.microsoft import MSBuildDeps, MSBuildToolchain
import os

class XsecConan(ConanFile):
    name = "xsec"
    description = "C++ cryptography library"
    author = "CSW <csw@werfen.com>"
    topics = ("conan", "crypto", "key")
    settings = "os", "compiler", "build_type", "arch"
    options = {"xerces_char_type" : ["uint16_t", "wchar_t"]}
    default_options = {"openssl/*:shared": True, "xerces-c/*:shared": True, "xerces_char_type": "uint16_t"}

    exports_sources = (
        "xsec/*",
        "Projects/*"
    )

    def requirements(self):
        self.requires("zlib/1.3.1", override = True)
        self.requires("openssl/3.0.16")
        self.requires("xerces-c/3.3.0")

    def config_options(self):
        self.options["xerces-c"].char_type = self.options.xerces_char_type

    def generate(self):
        msbuild_deps = MSBuildDeps(self)
        msbuild_deps.generate()

        msbuild_tc = MSBuildToolchain(self)
        msbuild_tc.generate()

    def package(self):
        copy(self, "*.hpp", dst=os.path.join(self.package_folder, "include", "xsec"), src=os.path.join(self.source_folder, "xsec"))
        copy(self, "*.h", dst=os.path.join(self.package_folder, "include", "xsec"), src=os.path.join(self.source_folder, "xsec"))

        source = os.path.join(self.source_folder, "Build", "Win32", f"VC{str(self.settings.compiler.version)}", f"{str(self.settings.build_type)} Minimal")

        copy(self, "xsec_lib.lib", dst=os.path.join(self.package_folder, "lib"), src=source)
        copy(self, "xsec_lib.dll", dst=os.path.join(self.package_folder, "bin"), src=source)
        copy(self, "xsec_lib.pdb", dst=os.path.join(self.package_folder, "bin"), src=source)

    def imports(self):
        copy(self, "*.dll", dst=os.path.join(self.build_folder, "bin"), src="bin")

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
        self.cpp_info.bindirs = ['bin']