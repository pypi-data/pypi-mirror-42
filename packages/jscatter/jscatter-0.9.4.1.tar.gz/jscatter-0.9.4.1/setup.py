# -*- coding: utf-8 -*-
import setuptools
import os
import glob
import numpy.distutils.core
# noinspection PyProtectedMember
from numpy.distutils.fcompiler import get_default_fcompiler

# this is to get the __version__ from version.py
with open('jscatter/version.py', 'r') as f:  exec(f.read())

with open('README.rst') as readme_file:
    long_description = readme_file.read()

# find fortran files
fs = glob.glob(os.path.join('jscatter', 'source', '*.f95'))
fs.sort()
EXTENSIONS = []
if get_default_fcompiler(requiref90=True):
    EXTENSIONS.append(numpy.distutils.core.Extension(name='jscatter.fscatter',
                                                     sources=fs,
                                                     extra_f90_compile_args=['-fopenmp'],
                                                     libraries=['gomp'],
                                                     # extra_f90_compile_args=['--debug','-fbounds-check'],
                                                     # f2py_options=['--debug-capi']
                                                     ))


def getfilenamelist(destination, exfolder, path):
    """create list of tuple of later destination with actual path"""
    llist = []
    for dp, dn, filenames in os.walk(os.path.join(exfolder, path)):
        for f in filenames:
            newdp = ''.join(dp.split(exfolder)[1:])
            if newdp[0] == '/': newdp = newdp[1:]
            llist.append((os.path.join(destination, newdp), [os.path.join(dp, f)]))
    return llist


# create the tuples for the data_files
datafiles = []
datafiles += getfilenamelist('jscatter/examples', 'jscatter/examples', 'exampleData')
datafiles += getfilenamelist('jscatter/doc', 'jscatter/doc', 'html')
datafiles += getfilenamelist('jscatter', 'jscatter', 'source')
datafiles += getfilenamelist('jscatter', 'jscatter', 'lib')
datafiles += getfilenamelist('jscatter', 'jscatter', 'data')
description=("Combines dataArrays with attributes for fitting, plotting" 
             "and analysis including models for Xray and neutron scattering")

numpy.distutils.core.setup(name='jscatter',
                           version=__version__,
                           description=description,
                           long_description=long_description,
                           author='Ralf Biehl',
                           author_email='ra.biehl@fz-juelich.de',
                           url='https://gitlab.com/biehl/jscatter',
                           platforms=["linux", "osx"],
                           classifiers=[
                               'Development Status :: 4 - Beta',
                               'Intended Audience :: Science/Research',
                               'Operating System :: POSIX :: Linux',
                               'Operating System :: MacOS :: MacOS X',
                               'Programming Language :: Python :: 2.7',
                               'Programming Language :: Python :: 3.5',
                               'Programming Language :: Python :: 3.6',
                               'Programming Language :: Python :: 3.7',
                               'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                               'Programming Language :: Python',
                               'Topic :: Scientific/Engineering :: Physics',
                           ],
                           include_package_data=True,
                           py_modules=[],
                           packages=setuptools.find_packages(exclude=['build']),
                           package_data={'': ['*.txt', '*.rst', '*.dat', '*.html']},
                           data_files=datafiles,
                           # cmdclass = {  },
                           dependency_links=[''],
                           install_requires=["numpy >= 1.8 ",
                                             "scipy >= 0.13",
                                             "matplotlib",
                                             "Pillow >= 5.2"],
                           ext_modules=EXTENSIONS,
                           test_suite='jscatter.test.suite'
                           )
