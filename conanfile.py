from conans import ConanFile, tools
import os
import shutil

class QtPropertyBrowserConan(ConanFile):
    name = "qt-propertybrowser"
    version = "1.0"
    generators = "qmake"
    settings = "os", "arch", "compiler", "build_type"

    options = {"shared": [True, False]}
    default_options = "shared=True"

    license = "Copyright ??"
    description = "collection of qt widgets"

    requires = (
            "qt/5.12.4-r2@camposs/stable",
    )

    scm = {
        "type": "git",
        "subfolder": "source",
        "url": "https://github.com/ulricheck/qt-solutions.git",
        "revision": "master",
        "submodule": "recursive",
    }



    def build(self):
        folder_name = os.path.join("source", "qtpropertybrowser")
        open(os.path.join(folder_name, "config.pri"), "w").write("SOLUTIONS_LIBRARY = yes")
        tools.replace_in_file(os.path.join(folder_name, "qtpropertybrowser.pro"), 
            """CONFIG += ordered""",
            """CONFIG += ordered
CONFIG += conan_basic_setup
include(../../conanbuildinfo.pri)"""
            )
        self.run( "cd %s && qmake CONFIG+=debug_and_release" % folder_name, run_environment=True)
        if self.settings.compiler == "Visual Studio":
            if self.settings.build_type == "Debug":
                self.run( "cd %s && nmake debug" % folder_name, run_environment=True )
            else:
                self.run( "cd %s && nmake release" % folder_name, run_environment=True )
        else:
            if self.settings.build_type == "Debug":
                self.run( "cd %s && make debug" % folder_name, run_environment=True )
            else:
                self.run( "cd %s && make release" % folder_name, run_environment=True )

    def package(self):
        self.copy(pattern="*.h", dst="include", src=os.path.join("source", "qtpropertybrowser", "src"))
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
