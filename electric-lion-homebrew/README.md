# Homebrew ROS Electric Install

## Prerequisites

First, this guide assumes you have a clean lion install, meaning no macports or homebrew previously setup.  In fact best results would come from a fresh format and install.  If you have macports (for something else) then make sure any macports specific references are commented out in your bashrc or bash_profile.  Then for good measure I recommend `sudo mv /opt /_opt` to make sure there is no cross talk.

### If you are updating your setup

If you are updating your setup from the first post, you will want to uninstall some things

    brew uninstall pil sip python

You will also want to take note of the changes in the ~/.bashrc lines you are supposed to use.

You will want to also make sure you are using the correct version of pip.  If not remove it and reinstall it.  You will need to also re-install pyyaml.

Additionally, the patches have been update to patch to the latest rosinstall url results (1.6.1).  So you will probably want to blow away your ros folder and do rosinstall from scratch so that the patches will apply cleanly.

There is also a Patching Homebrew section now, because I have several brew Formula patches that haven't quite made it up stream yet.

## Install Xcode 4

You can install Xcode 4 from the app store in lion, it is free, but a large download.  It is required before moving forward.

## Setup Homebrew

Install Homebrew

    /usr/bin/ruby -e "$(curl -fsSL https://raw.github.com/gist/323731)"

Make /Library directories writable in Lion (optional but highly recommended. Prevents you from needing sudo when you run pip in the future):

    sudo chown -R $USER /Library/Ruby /Library/Perl /Library/Python

## Pre-ROS Setup

Install some necessary tools. (git and svn are included by default with Xcode!)

    brew install wget cmake

Update you environment to use Homebrew kegs (packages) as the default by adding these lines to your ~/.bashrc

    export CPLUS_INCLUDE_PATH="/usr/local/include:$CPLUS_INCLUDE_PATH"

And make it so by closing and opening your terminal or with this line

    . ~/.bashrc

Install pip

    easy_install pip

Install Mercurial

    pip install Mercurial

Install libyaml

    brew install libyaml --universal

Install pyyaml

    pip install pyyaml

## Get ROS

The following lines will download the ROS source code using the rosinstall tool, and bootstrap the installation. The installation downloads all ROS stacks in subdirectories inside the ~/ros directory, one subdirectory for each stack in the rosinstall file.

First install rosinstall:

    pip install rosinstall

There are many different libraries and tools in ROS. We provided four default configurations to get you started.

**Desktop-Full Install (Recommended):** ROS Full, rviz, robot-generic libraries, 2D/3D simulators, navigation and 2D/3D perception

    rosinstall -n ~/ros "http://packages.ros.org/cgi-bin/gen_rosinstall.py?rosdistro=electric&variant=desktop-full&overlay=no"

**Desktop Install:** ROS Full, rviz, and robot-generic libraries

    rosinstall -n ~/ros "http://packages.ros.org/cgi-bin/gen_rosinstall.py?rosdistro=electric&variant=desktop&overlay=no"

**ROS-Full:** ROS package, build, communication, and graphical tools.

    rosinstall -n ~/ros "http://packages.ros.org/cgi-bin/gen_rosinstall.py?rosdistro=electric&variant=ros-full&overlay=no"

**ROS-Base:** (Bare Bones) ROS package, build, and communication libraries.

    rosinstall -n ~/ros "http://packages.ros.org/cgi-bin/gen_rosinstall.py?rosdistro=electric&variant=ros-base&overlay=no"

NOTE: the instructions above download all stacks inside the ~/ros folder. If you prefer a different location, simply change the ~/ros in the commands above.

## Patch ROS (Temporary)

Source ROS's setup file

    echo "source ~/ros/setup.bash" >> ~/.bashrc
    . ~/.bashrc

Checkout my ros-osx repository

    git clone git://github.com/wjwwood/ros-osx.git

Run the script to patch ROS

    cd ros-osx/electric-lion-homebrew
    python apply-patches.py ./patches $ROS_WORKSPACE

## Build ROS

Build the core ros stack, ros communications stack, and the common messages stack

    rosmake --rosdep-install ros ros_comm common_msgs

## Building stacks/packages you need

You can build additional stacks and packages with this form of command

    rosmake --rosdep-install <stacks and/or packages name>

The following stacks are known to build:

* assimp
* bond_core
* bullet
* common_msgs
* common_rosdeps
* common_tutorials
* diagnostics
* diagnostics_monitors
* driver_common
* eigen
* executive_smach
* executive\_smach_visualization
* filters
* geometry
* geometry_experimental
* image_common
* image_pipeline
* image\_transport_plugins
* laser_pipeline
* nodelet_core
* orocos\_kinematics_dynamics
* robot_model
* perception_pcl
    * This requires a patch that breaks the visualizers ability to take keyboard presses, so this is arguably not working, but I am going to take a stab this later.
* pluginlib
* ros
* ros_comm
* ros_tutorials
* vision_opencv
* xacro

The following are known not to build, and why:

* navigation
    * rosdep's failed to install: the netpbm build fails
* physics_ode
    * opende fails with:

    Please make sure that you use automake 1.10 or later
    Warnings about underquoted definitions are harmless
    Running aclocal
    /usr/bin/gm4:configure.in:373: bad expression in eval (bad input): 30 > libccd@:>@ 
    autom4te: /usr/bin/gm4 failed with exit status: 1
    aclocal: /usr/bin/autom4te failed with exit status: 1
    make[1]: *** [installed] Error 1

* simulator_gazebo
    * opende fails
* simulator_stage
    * stage fails
* slam_gmapping
    * netpbm
* stage
    * stage fails with:

    patch -d build/Stage-3.2.2-Source -p0 < Stage-3.2.2-Source.patch;
    patch: **** rejecting file name with ".." component: ../Stage-3.2.2-Source/libstage/CMakeLists.txt
    make[1]: *** [build/Stage-3.2.2-Source/unpacked] Error 2

Other known dependency issues:

* netpbm
    * doesn't build
* graphicsmagick  (is this needed?  it is on vision_opencv)
    * Fails

