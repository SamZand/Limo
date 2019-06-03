cmake_minimum_required(VERSION 3.0.0)
project(lemonator)

set(cxxflags ${CMAKE_CXX_FLAGS}
    -std=c++17
    # Note that gnu++11 instead of c++11 is used. This is required
    # because pybind11 expects a strdup function to be defined in the std.

    -Wall
    -Wextra
    # -pedantic-errors
    -Wfatal-errors
    -Wcast-align
    # -Wmissing-declarations

    # -Wredundant-decls
    # Note that pybind11 has redundant declarations, so this warning must be omitted.

    -Wuninitialized
    -Wno-unused-parameter
    -Wno-missing-field-initializers
    -Wno-pessimizing-move
    -Wno-redundant-move

    -Wno-cast-function-type

    # -Weffc++
    # Note that pybind11 is not writting using effc++

    -pthread
    -m64
    -DMS_WIN64
    -D_hypot=hypot
)

string(REGEX REPLACE ";" " " cxxflags "${cxxflags}")
set(CMAKE_CXX_FLAGS ${cxxflags})

set(PYBIND11_LTO_CXX_FLAGS "")
set(PYTHON_MODULE_EXTENSION ".pyd")

include_directories(include/)

add_subdirectory(lib/pybind11/)
pybind11_add_module(${PROJECT_NAME} MODULE src/main.cpp)

set(sources
    src/main.cpp
)