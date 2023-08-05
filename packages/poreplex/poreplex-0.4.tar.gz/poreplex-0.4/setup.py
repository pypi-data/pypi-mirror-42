#!/usr/bin/env python3
#
# Copyright (c) 2018-2019 Institute for Basic Science
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from setuptools import setup
from distutils.core import Extension
import numpy

extra_dependencies_live = ['inotify >= 0.2.9']

scrappie_sources = """
    src/contrib/scrappie/event_detection.c
""".split()

mod_csupport = Extension('poreplex.csupport',
                         sources=['src/csupport.c'] + scrappie_sources,
                         include_dirs=['src/contrib/scrappie', numpy.get_include()],
                         extra_compile_args=["-std=c99"])

setup(
    name='poreplex',
    packages=['poreplex'],
    version='0.4',
    description='A versatile sequence read processor for nanopore direct RNA sequencing',
    author='Hyeshik Chang',
    author_email='hyeshik@snu.ac.kr',
    url='https://github.com/hyeshik/poreplex',
    download_url='https://github.com/hyeshik/poreplex/releases',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords=[
        'nanopore',
        'direct RNA sequencing',
        'barcode',
        'demultiplexing'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    install_requires=[
        'PyYAML >= 3.0',
        'h5py >= 2.7.0',
        'mappy >= 2.10',
        'numpy >= 1.14',
        'pandas >= 0.22.0',
        'pomegranate >= 0.10',
        'progressbar33 >= 2.4',
        'pysam >= 0.14.0',
        'scipy >= 1.0',
        'urwid >= 2.0.0',
        'tensorflow >= 1.8.0',
        'Keras >= 2.1.6'
    ],
    extras_require={
        'live': extra_dependencies_live,
        'full': extra_dependencies_live,
    },
    entry_points={
        'console_scripts': [
            'poreplex = poreplex.commandline:__main__'
        ],
    },
    ext_modules=[mod_csupport],
)
