from conans import ConanFile, CMake, tools, RunEnvironment
import os

class BenchmarkConanPackageTest(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    build_policy = "missing"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        for ext in (".dll", ".pdb"):
            self.copy(pattern="*{!s}".format(ext), dst="bin", src="bin")
        for ext in (".lib", ".a", ".so*", ".dylib*"):
            self.copy(pattern="*{!s}".format(ext), dst="lib", src="lib")

    #def test(self):
        #self.run(os.sep.join([".", "bin", "BenchmarkPackageTest"]))

    def test(self):
        with tools.environment_append(RunEnvironment(self).vars):
            bin_path = os.path.join("bin", "BenchmarkPackageTest")
            if self.settings.os == "Windows":
                self.run(bin_path)
            elif self.settings.os == "Macos":
                self.run("DYLD_LIBRARY_PATH=%s %s" % (os.environ.get("DYLD_LIBRARY_PATH", ""), bin_path))
            else:
                self.run("LD_LIBRARY_PATH=%s %s" % (os.environ.get("LD_LIBRARY_PATH", ""), bin_path))
