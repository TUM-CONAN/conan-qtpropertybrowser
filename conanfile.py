from conans import ConanFile, CMake, tools
import os
import shutil

class QuickQanavaBrowserConan(ConanFile):
    name = "qt-quickqanava"
    version = "1.0"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"

    options = {"shared": [True, False]}
    default_options = "shared=True"

    license = "Copyright benoit@destrat.io BSD"
    description = "C++14 network/graph visualization library / Qt node editor."

    requires = (
            "qt/5.12.4-r2@camposs/stable",
    )

    scm = {
        "type": "git",
        "subfolder": "source",
        "url": "https://github.com/ulricheck/QuickQanava.git",
        "revision": "master",
        "submodule": "recursive",
    }

    def _cmake_configure(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SAMPLES"] = 'ON'
        cmake.definitions["BUILD_STATIC_QRC"] = 'ON'
        cmake.configure(source_dir='source')
        return cmake


    def build(self):
        tools.replace_in_file(os.path.join("source", "src", "CMakeLists.txt"),
            """set(DESTDIR "${QT_INSTALL_QML}/${TARGETPATH}")""",
            """set(DESTDIR "${CMAKE_INSTALL_PREFIX}/qml/${TARGETPATH}")""",
            )
        cmake = self._cmake_configure()
        cmake.build()
        # self.run( "cd %s && qmake CONFIG+=debug_and_release" % folder_name, run_environment=True)
        # if self.settings.compiler == "Visual Studio":
        #     if self.settings.build_type == "Debug":
        #         self.run( "cd %s && nmake debug" % folder_name, run_environment=True )
        #     else:
        #         self.run( "cd %s && nmake release" % folder_name, run_environment=True )
        # else:
        #     if self.settings.build_type == "Debug":
        #         self.run( "cd %s && make debug" % folder_name, run_environment=True )
        #     else:
        #         self.run( "cd %s && make release" % folder_name, run_environment=True )

    def package(self):
        cmake = self._cmake_configure()
        cmake.install()

        # for now also copy examples
        self.copy("*", dst="bin", src="bin")
        self.copy("*.qrc", dst="samples", src=os.path.join(self.source_folder, "source", "samples"))
        self.copy("*.qml", dst="samples", src=os.path.join(self.source_folder, "source", "samples"))
        self.copy("*.jpeg", dst="samples", src=os.path.join(self.source_folder, "source", "samples"))
        self.copy("*.jpg", dst="samples", src=os.path.join(self.source_folder, "source", "samples"))
        self.copy("*.conf", dst="samples", src=os.path.join(self.source_folder, "source", "samples"))


        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
