#!/usr/bin/env python
import sys
import os
import roslib.stacks
from copy import copy
import optparse
import logging; logger = logging.getLogger()

FORMAT = '%(levelname)-7s: %(message)s'
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)

original_dir = os.getcwd()

if not len(sys.argv) > 2:
    logger.error("Usage: python apply-patches.py <path to patches> <path to ros>")
    sys.exit(-1)
path_to_patches = os.path.abspath(sys.argv[1])
path_to_ros = os.path.abspath(sys.argv[2])
# path_to_ros = "/Users/william/devel/ros"
# path_to_patches = "/Users/william/devel/osx-ros/electric-lion-homebrew/patches"
# path_to_patches = "/tmp/patch_output-1.6.1"

logger.info("Using patches path: {0}".format(path_to_patches))
logger.info("Using ROS path: {0}".format(path_to_ros))

patches = os.listdir(path_to_patches)
try:
    os.chdir(path_to_patches)
except OSError as err:
    logger.error("Error entering {0}: {1}".format(path_to_patches, str(err)))
    sys.exit(-1)
for item in copy(patches):
    if not os.path.isfile(item):
        logger.debug("Ignoring {0}".format(item))
        patches.remove(item)

def generate_stack_version(name):
    """docstring for generate_stack_version"""
    import subprocess
    # This first method doesn't work on Python 2.6
    #temp = subprocess.check_output([os.path.join(path_to_ros, "ros/bin/rosversion"), name]).strip()
    temp = subprocess.Popen([os.path.join(path_to_ros, "ros/bin/rosversion"), name], stdout=subprocess.PIPE).communicate()[0]
    return temp

def svn_apply_patch(patch):
    """docstring for svn_generate_patch"""
    os.system("patch -p0 < {0}".format(patch))

def git_apply_patch(patch):
    """docstring for git_generate_patch"""
    os.system("git apply {0}".format(patch))

def hg_apply_patch(patch):
    """docstring for hg_generate_patch"""
    os.system("hg import --no-commit {0}".format(patch))

try:
    os.chdir(path_to_ros)
except OSError as err:
    logger.error("Error entering {0}: {1}".format(path_to_ros, str(err)))
    sys.exit(-1)
for patch in patches:
    os.chdir(path_to_ros)
    patch_info = patch.split('-')
    if len(patch_info) != 4 or patch_info[2] != "homebrew" or patch_info[3].split('.')[0] not in ["svn", "git", "hg"]:
        logger.error("Patch {0} is malformed, must conform to: <stack name>-<stack version>-homebrew-<vcs name>.patch".format(patch))
        continue
    
    stack_name = patch_info[0]
    stack_version = patch_info[1]
    try:
        stack_dir = roslib.stacks.get_stack_dir(stack_name)
    except:
        logger.warning("skipping patches for stack {0}: stack is not installed".format(stack_name))
        continue
    if stack_version != generate_stack_version(stack_name):
        logger.warning("Patch for stack {0} is for version {1} but the stack is of version {2}".format(stack_name, stack_version, generate_stack_version(stack_name)))
    vcs_type = patch_info[3].split('.')[0]
    
    try:
        os.chdir(stack_name)
    except OSError as err:
        logger.error("Error entering {0}: {1}".format(path_to_patches, str(err)))
    logger.debug("Entering folder {0}".format(os.getcwd()))
    
    if vcs_type == "svn":
        logger.debug("{0} is SVN".format(stack_name))
        svn_apply_patch(os.path.join(path_to_patches, patch))
    elif vcs_type == "git":
        logger.debug("{0} is Git".format(stack_name))
        git_apply_patch(os.path.join(path_to_patches, patch))
    elif vcs_type == "hg":
        logger.debug("{0} is Mercurial".format(stack_name))
        hg_apply_patch(os.path.join(path_to_patches, patch))
    else:
        logger.error("{0} is not a valid patch, no vcs detected.".format(folder))
    
    logger.debug("Exiting folder {0}".format(os.getcwd()))

os.chdir(original_dir)
logger.info("Done.")