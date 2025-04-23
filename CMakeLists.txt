cmake_minimum_required(VERSION 3.14)
project(pyembed_example)

set(CMAKE_CXX_STANDARD 17)
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
# pybind11 liefert ein CMake‑Config, wenn via pip install
find_package(pybind11 CONFIG REQUIRED)

add_executable(main main.cpp)
target_link_libraries(main
    PRIVATE
        pybind11::embed
        Python3::Python
)
