#!/usr/bin/env python
import os
import platform
import sys

from setuptools import Extension, setup


def cmd1(strings):
    return os.popen(strings).readlines()[0][:-1]


def cmd2(strings):
    return cmd1(strings).split()


if platform.system() == 'Windows':
    if sys.maxsize > 2**32:  # 64bit
        ext_modules = [
            Extension(
                "_MeCab",
                ["MeCab_wrap.cxx"],
                include_dirs=["C:\Program Files\MeCab\sdk"],
                library_dirs=["C:\Program Files\MeCab\sdk"],
                libraries=["libmecab"]
            )
        ]
        data_files = [('lib\\site-packages\\', ["C:\Program Files\MeCab\\bin\libmecab.dll"])]
    else:  # 32bit
        ext_modules = [
            Extension(
                "_MeCab",
                ["MeCab_wrap.cxx"],
                include_dirs=["C:\Program Files (x86)\MeCab\sdk"],
                library_dirs=["C:\Program Files (x86)\MeCab\sdk"],
                libraries=["libmecab"]
            )
        ]
        data_files = [('lib\\site-packages\\', ["C:\Program Files (x86)\MeCab\\bin\libmecab.dll"])]

else:
    ext_modules = [
        Extension(
            "_MeCab",
            ["MeCab_wrap.cxx"],
            include_dirs=cmd2("mecab-config --inc-dir"),
            library_dirs=cmd2("mecab-config --libs-only-L"),
            libraries=cmd2("mecab-config --libs-only-l"))
    ]
    data_files = None

setup(
    name="mecab-python-windows",
    version="0.996.3",
    py_modules=["MeCab"],
    ext_modules=ext_modules,
    data_files=data_files,
    author='Yukino Ikegami',
    author_email='yknikgm@gmail.com',
    url='https://github.com/ikegami-yukino/mecab/tree/master/mecab/python',
    license='BSD, GPL or LGPL',
    platforms=['Windows'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: Japanese',
        'Intended Audience :: Science/Research',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing'
    ],
    description='Python wrapper for CaboCha: Japanese Dependency Structure Analyzer',
    long_description='''This is a python wrapper for CaboCha. It does not sopport Windows Python 64bit version.

    License
    ---------
    CaboCha is copyrighted free software by Taku Kudo <taku@chasen.org>
is released under any of the the LGPL (see the file LGPL) or the
BSD License (see the file BSD).
    '''
)
