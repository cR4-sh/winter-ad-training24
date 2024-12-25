cmake_minimum_required(VERSION 3.10)
project(MINIONS)

set(CMAKE_C_COMPILER "/usr/bin/gcc")
add_executable(minions "src/main.c" "src/logic.c" "src/minions.c" "src/utils.c")

# No pie bebebe
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -no-pie")

# No canary bebebe
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fno-stack-protector")

target_include_directories(minions PUBLIC "headers")
