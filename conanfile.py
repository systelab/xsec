from conans import ConanFile, tools


class XsecConan(ConanFile):
	name = "xsec"
	description = "C++ cryptography library"
	author = "CSW <csw@werfen.com>"
	topics = ("conan", "crypto", "key")
	generators = "visual_studio"
	settings = "os", "compiler", "build_type", "arch"
	options = {"xerces_char_type" : ['uint16_t', 'wchar_t']}
	default_options = "openssl:shared=True", "xerces-c:shared=True", "xerces_char_type=uint16_t"

	def requirements(self):
		self.requires("zlib/1.3.1@#f52e03ae3d251dec704634230cd806a2", override = True)
		self.requires("openssl/3.0.16@#c4f4f2909b2327e1e8abec3748c1023f")
		self.requires("xerces-c/3.3.0#1460e1dcbd206b18a0ecf29f0b5ee361")

	def config_options(self):
		self.options["xerces-c"].char_type = self.options.xerces_char_type

	def package(self):
		self.copy("*.hpp", dst="include/xsec", src="xsec")
		self.copy("*.h", dst="include/xsec", src="xsec")
		self.copy("xsec_lib.lib", dst="lib", src=("Build/Win32/VC%s/%s Minimal" % (self.settings.compiler.version, self.settings.build_type)))
		self.copy("xsec_lib.dll", dst="bin", src=("Build/Win32/VC%s/%s Minimal" % (self.settings.compiler.version, self.settings.build_type)))
		self.copy("xsec_lib.pdb", dst="bin", src=("Build/Win32/VC%s/%s Minimal" % (self.settings.compiler.version, self.settings.build_type)))

	def imports(self):
		self.copy("*.dll", dst="../../../../../../Build/Win32/VC%s/%s Minimal" % (self.settings.compiler.version, self.settings.build_type), src="bin")

	def package_info(self):
		self.cpp_info.libs = tools.collect_libs(self)
		self.cpp_info.bindirs = ['bin']