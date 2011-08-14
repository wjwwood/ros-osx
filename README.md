# Homebrew ROS Electric Install

## Prerequisites

First, this guide assumes you have a clean lion install, meaning no macports or homebrew previously setup.  In fact best results would come from a fresh format and install.  If you have macports (for something else) then make sure any macports specific references are commented out in your bashrc or bash_profile.  Then for good measure I recommend `sudo mv /opt /_opt` to make sure there is no cross talk.

## Install Xcode 4

You can install Xcode 4 from the app store in lion, it is free, but a large download.  It is required before moving forward.

## Setup Homebrew

1. Install Homebrew

    /usr/bin/ruby -e "$(curl -fsSL https://raw.github.com/gist/323731)"

2. Make /Library directories writable in Lion (optional but recommended. Prevents you from needing sudo in the future):

    sudo chown -R $USER /Library/Ruby /Library/Perl /Library/Python

3. Make Ruby gems install executables to /usr/local/bin:

    ruby -C$HOME -ryaml -e "
    gemrc = YAML::load_file('.gemrc') rescue {}
    gemrc['gem'] = '-n/usr/local/bin'
    YAML::dump(gemrc, File.new('.gemrc', 'w'))"

## Pre-ROS Setup

Install some necessary tools.

    brew install git wget cmake subversion python

Update you environment to use Homebrew kegs (packages) as the default by adding these lines to your ~/.bashrc

    export PATH="/usr/local/share/python:/usr/local/bin:$PATH"
    export PKG_CONFIG_PATH="/usr/local/share/pkgconfig:$PKG_CONFIG_PATH"

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

    cd ros-osx
    bash patch-ros.sh $ROS_WORKSPACE

## Build ROS

Build the core ros stack, ros communications stack, and the common messages stack

    rosmake --rosdep-install ros ros_comm common_msgs

## Building stacks/packages you need

You can build additional stacks and packages with this form of command

    rosmake --rosdep-install <stack or package name>

The following stacks are known to work:

* ros
* ros_comm
* common_msgs
