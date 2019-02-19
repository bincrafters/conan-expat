#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import ConanFile, CMake, tools


class ExpatConan(ConanFile):
    name = "expat"
    version = "2.2.5"
    description = "Fast XML parser in C"
    url = "https://github.com/bincrafters/conan-expat"
    homepage = "https://github.com/libexpat/libexpat"
    author = "Bincrafters <bincrafters@gmail.com>"
    topics = ("conan", "expat", "xml", "xml-parser")
    license = "MIT"
    exports = ['LICENSE.md']
    exports_sources = ['CMakeLists.txt']
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    @property
    def _is_mingw(self):
        return self.settings.os == "Windows" and self.settings.compiler == "gcc"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
        if self._is_mingw:
            del self.options.shared

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        sha256 = "b3781742738611eaa737543ee94264dd511c52a3ba7e53111f7d705f6bff65a8"
        tools.get("{}/archive/R_{}.tar.gz".format(self.homepage, self.version.replace('.', '_')), sha256=sha256)
        extracted_folder = "libexpat-R_" + self.version.replace('.', '_')
        os.rename(extracted_folder, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_doc'] = False
        cmake.definitions['BUILD_examples'] = False
        cmake.definitions['BUILD_tests'] = False
        cmake.definitions['BUILD_tools'] = False
        if not self._is_mingw:
            cmake.definitions['BUILD_shared'] = self.options.shared
        cmake.configure(build_dir=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("COPYING", dst="licenses", src=os.path.join(self._source_subfolder, "expat"))
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if not self._is_mingw and not self.options.shared:
            self.cpp_info.defines = ["XML_STATIC"]

