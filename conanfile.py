import shutil

from conans import ConanFile, CMake, tools


class GoogleBenchmarkConan(ConanFile):
    name = "benchmark"
    version = "1.3.0"
    description = "A microbenchmark support library."
    url = "http://github.com/croydon/conan-google-benchmark"
    license = "Apache-2.0"
    settings = "arch", "build_type", "compiler", "os"
    options = {
        "enable_lto": [True, False],
        "enable_exceptions": [True, False],
        "shared": [True, False]
    }
    default_options = "enable_lto=False", "enable_exceptions=True", "shared=False"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    build_policy = "missing"

    def source(self):
        archive_url = "https://github.com/google/benchmark/archive/v{!s}.zip".format(self.version)
        tools.get(archive_url, sha256="51c2d2d35491aea83aa6121afc4a1fd9262fbd5ad679eb5e03c9fa481e42571e")
        shutil.move("benchmark-{!s}".format(self.version), "benchmark")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
        cmake.definitions["BENCHMARK_ENABLE_TESTING"] = "OFF"
        cmake.definitions["BENCHMARK_ENABLE_LTO"] = "ON" if self.options.enable_lto else "OFF"
        cmake.definitions["BENCHMARK_ENABLE_EXCEPTIONS"] = "ON" if self.options.enable_exceptions else "OFF"
        if str(self.settings.compiler.libcxx) == "libc++":
            cmake.definitions["BENCHMARK_USE_LIBCXX"] = "ON"
        else:
            cmake.definitions["BENCHMARK_USE_LIBCXX"] = "OFF"

        # See https://github.com/google/benchmark/pull/523
        if self.settings.os != "Windows":
            cmake.definitions["BENCHMARK_BUILD_32_BITS"] = "ON" if "64" not in str(self.settings.arch) else "OFF"

        cmake.configure()
        cmake.build()
        cmake.install()
        cmake.patch_config_paths()

    def package(self):
        self.copy(pattern="*.h", dst="include", src="include/benchmark", keep_path=False)
        self.copy(pattern="*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*", dst=".", src="lib/cmake/benchmark", keep_path=False)

    def package_info(self):
        # let consuming projects know what library name is used for linking
        self.cpp_info.libs = [self.name]
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["pthread", "rt"])
        if self.settings.os == "Windows":
            self.cpp_info.libs.append("shlwapi")
