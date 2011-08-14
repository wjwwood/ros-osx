#!/usr/bin/env bash

_CWD=`pwd`

cd $1

cd ros
patch -p0 < $_CWD/patches/ros-homebrew.patch

cd ../ros_comm
patch -p0 < $_CWD/patches/ros_comm-homebrew.patch
patch -p0 < $_CWD/patches/ros_comm-rosconsole-llvmsegfault-fix.patch

cd ../bullet
patch -p0 < $_CWD/patches/bullet-hombrew.patch

cd ../common_rosdeps
patch -p0 < $_CWD/patches/common_rosdeps-homebrew.patch

cd ../geometry
patch -p0 < $_CWD/patches/geometry-homebrew.patch

cd ../orocos_kinematics_dynamics
patch -p0 < $_CWD/patches/orocos_kinematics_dynamics-homebrew.patch
patch -p0 < $_CWD/patches/orocos_kinematics_dynamics-findeigen3.patch
patch -p0 < $_CWD/patches/orocos_kinematics_dynamics-pythonbindings.patch

cd $_CWD