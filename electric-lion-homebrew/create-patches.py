#!/usr/bin/env python
import sys
import os
from copy import copy
import optparse
import logging; logger = logging.getLogger()

FORMAT = '%(levelname)-7s: %(message)s'
logging.basicConfig(format=FORMAT)
# logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

original_dir = os.getcwd()
output_path = "/tmp/patch_output"
if not os.path.exists(output_path):
    os.mkdir(output_path)

# path = os.getcwd()
path = "/Users/william/devel/ros"
if len(sys.argv) > 1:
    path = sys.argv[1]

logger.info("Using path: {0}".format(path))

folders = os.listdir(path)
os.chdir(path)
for item in copy(folders):
    if not os.path.isdir(item):
        logger.debug("Ignoring {0}".format(item))
        folders.remove(item)

def svn_generate_patch(name):
    """docstring for svn_generate_patch"""
    os.system("svn diff > {0}/{1}-homebrew-svn.patch".format(output_path, name))

def git_generate_patch(name):
    """docstring for git_generate_patch"""
    os.system("git diff > {0}/{1}-homebrew-git.patch".format(output_path, name))

def hg_generate_patch(name):
    """docstring for hg_generate_patch"""
    os.system("hg diff > {0}/{1}-homebrew-hg.patch".format(output_path, name))

os.chdir(path)
for folder in folders:
    try:
        os.chdir(folder)
    except OSError as err:
        logger.error("Error entering {0}: {1}".format(folder, str(err)))
    logger.debug("Entering folder {0}".format(os.getcwd()))
    
    if os.path.exists(".svn"):
        logger.debug("{0} is SVN".format(folder))
        svn_generate_patch(folder)
    elif os.path.exists(".git"):
        logger.debug("{0} is Git".format(folder))
        git_generate_patch(folder)
    elif os.path.exists(".hg"):
        logger.debug("{0} is Mercurial".format(folder))
        hg_generate_patch(folder)
    else:
        logger.error("{0} is not under source control".format(folder))
    
    logger.debug("Exiting folder {0}".format(os.getcwd()))
    os.chdir(path)

os.chdir(original_dir)
logger.info("Done.")