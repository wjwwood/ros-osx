#!/usr/bin/env bash

_CWD=`pwd`

cd $1

patch -p0 < $_CWD/patches/ros-homebrew.patch
patch -p0 < $_CWD/patches/ros_comm-homebrew2.patch
patch -p0 < $_CWD/patches/ros_comm-rosconsole-llvmsegfault-fix.patch

cd $_CWD