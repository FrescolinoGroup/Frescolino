# general settings
cmake_minimum_required (VERSION 3.0)
project({LIBRARY_NAME})

enable_testing()

set(FSC_WEBSITE ${PROJECT_SOURCE_DIR}/../../website/frescolino)
set(CMAKE_MAJOR_VERSION 0)
set(CMAKE_MINOR_VERSION 0)
set(CMAKE_PATCH_VERSION 0)

# if additional cmake modules are needed
set(CMAKE_MODULE_PATH "/usr/include;/usr/local/include;~/.local/include;~/local/include;${PROJECT_SOURCE_DIR}")
include(softinstall)
include(explicit_instantiation)

# compiler & flags
set(CMAKE_CXX_COMPILER "g++")
set(CMAKE_CXX_FLAGS "-std=c++14 -O3 -march=native -Werror -Wall -Wextra -Wpedantic")
#~ set(CMAKE_CXX_COMPILER "clang++")
#~ set(CMAKE_CXX_FLAGS "-std=c++14 -O3 -march=native -Werror -Weverything -Wno-c++98-compat -Wno-c++98-compat-pedantic -Wno-missing-prototypes -Wno-exit-time-destructors -Wno-global-constructors -Wno-implicit-fallthrough -Wno-disabled-macro-expansion -Wno-documentation-unknown-command")

#~ set(CMAKE_EXE_LINKER_FLAGS "-pg")

# define variables

# uninstall target
configure_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/config/cmake_uninstall.cmake.in"
  "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake"
  IMMEDIATE @ONLY)

add_custom_target(uninstall
  COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake)

# include directories
include_directories(${PROJECT_SOURCE_DIR}/src)

# add subdirs
add_subdirectory(${PROJECT_SOURCE_DIR}/doc)
add_subdirectory(${PROJECT_SOURCE_DIR}/test)
add_subdirectory(${PROJECT_SOURCE_DIR}/example)
