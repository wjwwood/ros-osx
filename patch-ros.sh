#!/usr/bin/env bash

_CWD=`pwd`

cd $1

cd ros
patch -p0 < $_CWD/patches/ros-homebrew.patch

cd ../ros_comm
patch -p0 < $_CWD/patches/ros_comm-homebrew.patch
patch -p0 < $_CWD/patches/ros_comm-rosconsole-llvmsegfault-fix.patch

cd $_CWD