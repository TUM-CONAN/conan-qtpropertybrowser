from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os
import textwrap


class QtPropertyBrowserConan(ConanFile):
    name = "qt-propertybrowser"
    version = "2.0"
    settings = "os", "arch", "compiler", "build_type"


    generators = ["cmake", "cmake_find_package"]
    exports_sources = ["patches/**","CMakeLists.txt"]
    _cmake = None

    options = {
         "shared": [True, False],
         "fPIC": [True, False]
    }
    default_options = {
        "shared":      False,
        "fPIC": True
    }

    license = "Copyright by qt-solutions git repo"
    description = "qt property browser"

    scm = {
        "type": "git",
        "subfolder": "source_subfolder",
        "url": "https://github.com/TUM-CAMP-NARVIS/qtpropertybrowser.git",
        "revision": "main",
        "submodule": "recursive",
    }


    @staticmethod
    def _create_cmake_module_alias_targets(module_file, alias, aliased):
        content = ""
        content += textwrap.dedent("""\
            if(TARGET {aliased} AND NOT TARGET {alias})
                add_library({alias} INTERFACE IMPORTED)
                set_property(TARGET {alias} PROPERTY INTERFACE_LINK_LIBRARIES {aliased})
            endif()
        """.format(alias=alias, aliased=aliased))
        tools.save(module_file, content)

    @property
    def _module_subfolder(self):
        return os.path.join(
            "lib",
            "cmake"
        )

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_folder(self):
        return "build"

    @property
    def _pkg_share(self):
        return os.path.join(
            self.package_folder,
            "share"
        )

    @property
    def _pkg_etc(self):
        return os.path.join(
            self.package_folder,
            "etc"
        )
    
    @property
    def _pkg_res(self):
        return os.path.join(
            self.package_folder,
            "res"
        )

    @property
    def _pkg_cmake(self):
        return os.path.join(
            self.package_folder,
            "lib/cmake"
        )

    @property
    def _target_aliases(self):
        aliases = {
        }
        return aliases

    def _patch_sources(self):
        for patch in []:  #[{"base_path": self._source_subfolder, "patch_file":"patches/patch_gcc11_compatibility.patch",  "strip":0},]:
            tools.patch(**patch)

    def configure(self):
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC

    def config_options(self):
        pass
    
    def requirements(self):
        self.requires("qt/5.15.4")

    def validate(self):
        os = self.settings.os
        compiler = self.settings.compiler
        version = tools.Version(self.settings.compiler.version)
        if compiler.get_safe("cppstd"):
            tools.check_min_cppstd(self, 11)
        if compiler == "Visual Studio" and version < "16":
            raise ConanInvalidConfiguration(
                "QTpropertybrowser is just supported for Visual Studio compiler 16 and higher.")

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        if self.settings.compiler != 'Visual Studio':
            self._cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        self._cmake.configure()
        return self._cmake

    def build(self):
        self._patch_sources()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("LICENSE", src=self._source_subfolder, dst="licenses")
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
