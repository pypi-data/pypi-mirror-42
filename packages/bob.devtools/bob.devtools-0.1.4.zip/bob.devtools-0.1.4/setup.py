#!/usr/bin/env python

from setuptools import setup, find_packages

# Define package version
version = open("version.txt").read().rstrip()

requires = [
    'setuptools',
    'click>=7.0.0',
    'click-plugins',
    'conda-build>=3.0.0',
    'certifi',
    'requests',
    'gitpython',
    'python-gitlab',
    'sphinx',
    'pyyaml',
    'twine',
    'lxml',
    'jinja2',
    ]

setup(
    name="bob.devtools",
    version=version,
    description="Tools for development and CI integration of Bob/BEAT packages",
    url='http://gitlab.idiap.ch/bob/bob.devtools',
    license="BSD",
    author='Bob/BEAT Developers',
    author_email='bob-devel@googlegroups.com,beat-devel@googlegroups.com',
    long_description=open('README.rst').read(),

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    # when updating these dependencies, update the README too
    install_requires=requires,

    entry_points={
        'console_scripts': [
            'bdt = bob.devtools.scripts.bdt:main',
        ],
        'bdt.cli': [
          'release = bob.devtools.scripts.release:release',
          'new = bob.devtools.scripts.new:new',
          'changelog = bob.devtools.scripts.changelog:changelog',
          'lasttag = bob.devtools.scripts.lasttag:lasttag',
          'visibility = bob.devtools.scripts.visibility:visibility',
          'dumpsphinx = bob.devtools.scripts.dumpsphinx:dumpsphinx',
          'create = bob.devtools.scripts.create:create',
          'build = bob.devtools.scripts.build:build',
          'getpath = bob.devtools.scripts.getpath:getpath',
          'caupdate = bob.devtools.scripts.caupdate:caupdate',
          'ci = bob.devtools.scripts.ci:ci',
          ],

        'bdt.ci.cli': [
          'build = bob.devtools.scripts.ci:build',
          'clean = bob.devtools.scripts.ci:clean',
          'base-deploy = bob.devtools.scripts.ci:base_deploy',
          'deploy = bob.devtools.scripts.ci:deploy',
          'readme = bob.devtools.scripts.ci:readme',
          'pypi = bob.devtools.scripts.ci:pypi',
          ],
    },
    classifiers=[
        'Framework :: Bob',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
    ],
)
