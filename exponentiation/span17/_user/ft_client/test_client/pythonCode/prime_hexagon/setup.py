from glob import glob
import os
from setuptools import setup, Extension
from distutils.command.build_ext import build_ext
from distutils.command.build_clib import build_clib

import numpy
np_include_path = [numpy.get_include()]
c_options = {}
c_options['use_numpy'] = 1

def generate_cython_c_config_file():
    print('Generate config.pxi')
    d = os.path.dirname(__file__)
    config_file_name = os.path.join(  d , 'config.pxi')
    with open(config_file_name, 'w') as fd:
        for k, v in c_options.items():
            fd.write('DEF %s = %d\n' % (k.upper(), int(v)))

generate_cython_c_config_file()

# assume fallback to compiled cpp
EXT='cpp'
cythonize = None
if glob("*.pyx"):
    try:
        from Cython.Build import cythonize
        EXT = 'pyx'                 # file extension to use if cython is installed
    except:
        pass

extension = Extension(
        "primehexagon",
        ["primehexagon.{}".format(EXT)],
        include_dirs=[] + np_include_path,
        language="c++",
        )

ext_modules = cythonize(extension) if cythonize else [extension]

setup(
    name='primehexagon',
    version="0.1.0",
    url = "https://github.com/tsgallion/prime-hexagon",
    description="Exploring prime numbers on the hexagon",
    license = "MIT",
    ext_modules = ext_modules,
    py_modules = ['primespin'],
    install_requires=['numpy', 'primesieve'],
    classifiers=[
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    ],
)
