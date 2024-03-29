cmake_minimum_required(VERSION 3.0.0)
project(lemonator)

set(headers
    include/ds1820.hpp
    include/lemonator_interface.hpp
    include/py-interface.hpp
    include/sr04.hpp
    include/statemachine.hpp
    include/tcs3200.hpp
)

set(sources
    src/main.cpp
    src/statemachine.cpp
    ${headers}
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(cxxflags ${CMAKE_CXX_FLAGS}
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

include_directories(include/)

# hwlib
include_directories(${INCLUDE_DIRECTORIES} lib/hwlib/library)
# source_group(Headers TREE lib/hwlib/library)
add_subdirectory(lib/hwlib)
target_compile_options(hwlib INTERFACE
    -Wno-type-limits
)
target_compile_definitions(hwlib INTERFACE HWLIB_TARGET_pyd)
link_libraries(hwlib)

# RS232 library
add_library(rs232 STATIC lib/RS-232/rs232.c)
include_directories(${INCLUDE_DIRECTORIES} lib/RS-232)
# source_group(Headers TREE lib/RS-232)
link_libraries(rs232) 

# Pybind .pyd module
set(PYBIND11_LTO_CXX_FLAGS "")
set(PYTHON_MODULE_EXTENSION ".pyd")
set(PYBIND11_PYTHON_VERSION 3.5 CACHE STRING "")
add_compile_definitions(VERSION_INFO="0.0.2")
add_subdirectory(lib/pybind11/)
pybind11_add_module(${PROJECT_NAME} MODULE ${sources})

# Compile C++ executable
add_executable(cpp-only ${sources})
target_compile_definitions(cpp-only PUBLIC PYBIND_DISABLED)