cmake_minimum_required(VERSION 3.0.2)
project(drone)

set(CMAKE_CXX_FLAGS "-fpermissive -std=c++0x")

find_package(catkin REQUIRED)

catkin_package(DEPENDS)
