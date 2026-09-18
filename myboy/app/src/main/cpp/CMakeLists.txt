cmake_minimum_required(VERSION 3.22)
project(myboy_arm64_bridge LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(MGBA_PIN "25ca25612eb806ad3a70f3209ccd93890ea0c2c6"
    CACHE STRING "Pinned mGBA commit")

set(LIBMGBA_ONLY ON CACHE BOOL "" FORCE)
set(M_CORE_GBA ON CACHE BOOL "" FORCE)
set(M_CORE_GB OFF CACHE BOOL "" FORCE)
set(ENABLE_DEBUGGERS OFF CACHE BOOL "" FORCE)
set(ENABLE_SCRIPTING OFF CACHE BOOL "" FORCE)
set(USE_LUA OFF CACHE BOOL "" FORCE)
set(USE_FFMPEG OFF CACHE BOOL "" FORCE)
set(USE_PNG OFF CACHE BOOL "" FORCE)
set(USE_LIBZIP OFF CACHE BOOL "" FORCE)
set(USE_SQLITE3 OFF CACHE BOOL "" FORCE)
set(USE_JSON_C OFF CACHE BOOL "" FORCE)
set(BUILD_STATIC ON CACHE BOOL "" FORCE)
set(BUILD_SHARED OFF CACHE BOOL "" FORCE)

set(MGBA_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/third_party/mgba")
if(EXISTS "${MGBA_SOURCE_DIR}/CMakeLists.txt")
    add_subdirectory("${MGBA_SOURCE_DIR}" "${CMAKE_CURRENT_BINARY_DIR}/mgba")
else()
    include(FetchContent)
    FetchContent_Declare(
        mgba_src
        GIT_REPOSITORY https://github.com/mgba-emu/mgba.git
        GIT_TAG        ${MGBA_PIN}
        GIT_SHALLOW    FALSE
    )
    FetchContent_MakeAvailable(mgba_src)
endif()

target_compile_definitions(mgba PRIVATE COLOR_16_BIT COLOR_5_6_5)
set_property(TARGET mgba PROPERTY POSITION_INDEPENDENT_CODE ON)

add_library(gba SHARED
    myboy_jni_bridge.cpp
    mgba_core_bridge.cpp
)

target_include_directories(gba PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}")
target_compile_features(gba PRIVATE cxx_std_20)
target_compile_definitions(gba PRIVATE COLOR_16_BIT COLOR_5_6_5 ENABLE_VFS)
target_compile_options(gba PRIVATE -Wall -Wextra -Wpedantic)

target_link_options(gba PRIVATE
    "-Wl,-z,max-page-size=16384"
    "-Wl,-z,common-page-size=16384"
)

find_library(log-lib log)
target_link_libraries(gba PRIVATE mgba ${log-lib})
