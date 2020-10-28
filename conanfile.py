from conans import ConanFile, Meson

class HelloConan(ConanFile):
    name = "sxplayer"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "pkg_config"
    exports_sources = "./*"
    requires = "ffmpeg/4.1-r7@sight/stable"

    def build(self):
        meson = Meson(self, backend="ninja")
        meson.configure(source_folder=".", build_folder=".", pkg_config_paths=".")
        meson.build()

    def package(self):
        self.copy("*.h", dst="include", src=".")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["sxplayer"]