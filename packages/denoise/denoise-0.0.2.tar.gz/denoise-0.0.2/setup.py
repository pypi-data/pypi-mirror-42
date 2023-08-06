#!/usr/bin/env python
# coding=utf-8
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

VERSION = "0.0.2"

sourcefiles = ["denoise.pyx", "src/utils.c", "src/rnnoise.c", "src/pitch.c", "src/rnn.c", "src/rnn_data.c", "src/celt_lpc.c"]

ext_modules = [
    Extension("denoise",
              sources=sourcefiles
              )
]

setup(name="denoise",
        version=VERSION,
        ext_modules=cythonize(ext_modules))
