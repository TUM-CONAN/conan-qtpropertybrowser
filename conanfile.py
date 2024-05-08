from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
from conan.tools.scm import Git
from conan.tools.files import load, update_conandata, copy, replace_in_file, collect_libs
from conan.tools.env import VirtualRunEnv, VirtualBuildEnv
import os

class QtPropertyBrowserConan(ConanFile):
    name = "qt-propertybrowser"
    version = "2.0"

    license = "Copyright by qt-solutions git repo"
    description = "qt property browser"

    settings = "os", "arch", "compiler", "build_type"
    options = {
         "shared": [True, False],
         "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True
    }

    def requirements(self):
        self.requires("qt/6.6.1@camposs/stable")
        # self.requires("libuuid/1.0.3")
        # self.requires("brotli/1.0.9")
        # self.requires("pcre2/10.42")
        # self.requires("libtool/2.4.7")
        # self.requires("automake/1.16.5")
        # self.requires("autoconf/2.71")
        # self.requires("m4/1.4.19")
        # self.requires("opengl/system")
        # self.requires("md4c/0.4.8")
        # self.requires("libffi/3.4.3")

        # if self.settings.os == "Linux":
        #     self.requires("xkbcommon/1.5.0")
        #     self.requires("xorg/system")
        #     self.requires("xkeyboard-config/system")
        #     self.requires("wayland/1.21.0")

    def export(self):
        update_conandata(self, {"sources": {
            "commit": "main",
            "url": "https://github.com/TUM-CAMP-NARVIS/qtpropertybrowser.git"
        }})

    def source(self):
        git = Git(self)
        sources = self.conan_data["sources"]
        git.clone(url=sources["url"], target=self.source_folder, args=["--recursive", ])
        git.checkout(commit=sources["commit"])

    def generate(self):
        tc = CMakeToolchain(self)

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            tc.variables[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)

        tc.generate()

        deps = CMakeDeps(self)
        deps.set_property("qt", "cmake_find_mode", "module")
        deps.set_property("qt", "cmake_file_name", "Qt6")
        deps.set_property("qt", "cmake_target_name", "qt::qt")

        # deps.set_property("brotli", "cmake_find_mode", "module")
        # deps.set_property("brotli", "cmake_file_name", "brotli")
        # deps.set_property("brotli", "cmake_target_name", "brotli::brotli")

        # deps.set_property("libuuid", "cmake_find_mode", "module")
        # deps.set_property("libuuid", "cmake_file_name", "libuuid")
        # deps.set_property("libuuid", "cmake_target_name", "libuuid::libuuid")

        # deps.set_property("libtool", "cmake_find_mode", "module")
        # deps.set_property("libtool", "cmake_file_name", "libtool")
        # deps.set_property("libtool", "cmake_target_name", "libtool::libtool")

        # deps.set_property("automake", "cmake_find_mode", "module")
        # deps.set_property("automake", "cmake_file_name", "automake")
        # deps.set_property("automake", "cmake_target_name", "automake::automake")

        # deps.set_property("autoconf", "cmake_find_mode", "module")
        # deps.set_property("autoconf", "cmake_file_name", "autoconf")
        # deps.set_property("autoconf", "cmake_target_name", "autoconf::autoconf")

        # deps.set_property("m4", "cmake_find_mode", "module")
        # deps.set_property("m4", "cmake_file_name", "m4")
        # deps.set_property("m4", "cmake_target_name", "m4::m4")

        # deps.set_property("xkbcommon", "cmake_find_mode", "module")
        # deps.set_property("xkbcommon", "cmake_file_name", "xkbcommon")
        # deps.set_property("xkbcommon", "cmake_target_name", "xkbcommon::xkbcommon")

        # deps.set_property("pcre2", "cmake_find_mode", "module")
        # deps.set_property("pcre2", "cmake_file_name", "PCRE2")
        # deps.set_property("pcre2", "cmake_target_name", "pcre2::pcre2")

        # deps.set_property("opengl", "cmake_find_mode", "module")
        # deps.set_property("opengl", "cmake_file_name", "opengl_system")
        # deps.set_property("opengl", "cmake_target_name", "opengl::opengl")

        # deps.set_property("md4c", "cmake_find_mode", "module")
        # deps.set_property("md4c", "cmake_file_name", "md4c")
        # deps.set_property("md4c", "cmake_target_name", "md4c::md4c")

        # deps.set_property("xorg", "cmake_find_mode", "module")
        # deps.set_property("xorg", "cmake_file_name", "xorg")
        # deps.set_property("xorg", "cmake_target_name", "xorg::xorg")

        # deps.set_property("wayland", "cmake_find_mode", "module")
        # deps.set_property("wayland", "cmake_file_name", "wayland")
        # deps.set_property("wayland", "cmake_target_name", "wayland::wayland")

        # deps.set_property("libffi", "cmake_find_mode", "module")
        # deps.set_property("libffi", "cmake_file_name", "libffi")
        # deps.set_property("libffi", "cmake_target_name", "libffi::libffi")

        # deps.set_property("xkeyboard-config", "cmake_find_mode", "module")
        # deps.set_property("xkeyboard-config", "cmake_file_name", "xkeyboard-config")
        # deps.set_property("xkeyboard-config", "cmake_target_name", "xkeyboard-config::xkeyboard-config")

        deps.generate()

    def layout(self):
        cmake_layout(self, src_folder="source_folder")

    def build(self):
        # overwritten since capnp needs to be able to find its shared lib if build with_shared
        cmake = CMake(self)
        env = VirtualRunEnv(self)
        with env.vars().apply():
            cmake.configure()
            cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)