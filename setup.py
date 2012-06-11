#!/usr/bin/python
# -*- coding: utf-8 -*-
# Distutils installer for PyJack

# Test for Jack2
#---------------------------------------------------#
import os
if os.path.exists("/usr/local/include/jack/jack.h"):
  path = "/usr/local/include/jack/jack.h"
elif os.path.exists("/usr/include/jack/jack.h"):
  path = "/usr/include/jack/jack.h"
else:
  print "You don't seem to have the jack headers installed.\nPlease install them first"
  exit(-1)

test = open(path).read()

if ("jack_get_version_string" in test):
  os.system("patch -f -s -p0 -r build/jack2.rej < ./patches/enable-jack2.diff > /dev/null")
else:
  os.system("patch -R -f -s -p0 -r build/jack2.rej < ./patches/enable-jack2.diff > /dev/null")
#----------------------------------------------------#


from distutils.core import setup, Extension
import numpy.distutils

numpy_include_dirs = numpy.distutils.misc_util.get_numpy_include_dirs()

setup(
    name = "pyjack",
    version = "0.5.1",
    description = "Python bindings for the Jack Audio Server",
    author = "Andrew W. Schmeder, falkTX",
    author_email = "andy@a2hd.com",
    url = "http://www.a2hd.com/software",

    ext_modules = [Extension("jack", ["pyjack.c"], libraries=["jack", "dl"], include_dirs=numpy_include_dirs)],
    )

