#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

ver_dic = {}
version_file_name = "gmsh_interop/version.py"
with open(version_file_name) as version_file:
    version_file_contents = version_file.read()

exec(compile(version_file_contents, version_file_name, 'exec'), ver_dic)

setup(name="gmsh_interop",
      version=ver_dic["VERSION_TEXT"],
      description="A parser for GMSH's .msh format",
      long_description=open("README.rst", "r").read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Other Audience',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Scientific/Engineering :: Visualization',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities',
          ],

      install_requires=[
          "six>=1.8.0",
          "numpy>=1.6.0",
          "pytools",
          ],

      author="Andreas Kloeckner",
      url="http://github.com/inducer/gmsh_interop",
      author_email="inform@tiker.net",
      license="MIT",
      packages=find_packages())
