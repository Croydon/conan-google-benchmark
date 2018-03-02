cmake_minimum_required(VERSION 3.0)

project(BenchmarkPackageTest
         VERSION       0.0.1
         LANGUAGES     C  CXX
)

set(CMAKE_CXX_STANDARD  11)
set(CMAKE_CXX_STANDARD_REQUIRED  OFF)
set(CMAKE_CXX_EXTENSIONS  OFF)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup(TARGETS)

add_executable(BenchmarkPackageTest
    main.cpp
)
target_link_libraries(BenchmarkPackageTest
    PRIVATE  CONAN_PKG::benchmark
)
