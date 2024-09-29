cmake_minimum_required(VERSION 3.0)
project(wasm_project)

set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -s")

add_executable(lockdoor.wasm "lockdoor.cpp")
add_executable(unlockdoor.wasm "unlockdoor.cpp")
add_executable(lighton.wasm "lighton.cpp")
add_executable(lightoff.wasm "lightoff.cpp")
add_executable(listen.wasm "listen.cpp")
add_executable(showcam.wasm "showcam.cpp")
add_executable(opencal.wasm "opencal.cpp")
add_executable(weather.wasm "weather.cpp")
add_executable(removescript.wasm "removescript.cpp")