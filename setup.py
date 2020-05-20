#!/usr/bin/env python3
import os
from setuptools import find_packages, setup

SETUP_DIR = os.path.dirname(__file__)
README = os.path.join(SETUP_DIR, 'README.rst')

setup(
    name='c2wl_rocket',
    version='0.0.1',    
    description="""
        A highly flexible CWL runner with customizeable task execution, 
        especially suited for deployment in the cloud.
    """,
    long_description=open(README).read(),
    long_description_content_type="text/x-rst",
    url='https://github.com/KerstenBreuer/C2WL-Rocket',
    download_url="https://github.com/KerstenBreuer/C2WL-Rocket",
    author='Kersten Henrik Breuer',
    author_email='kersten-breuer@live.de',
    license='Apache 2.0',
    include_package_data=True,
    packages=find_packages(exclude=("test_out", "tests", ".vscode" ".pytest_cache")),
    entry_points={
        "console_scripts": [
            "c2wl_rocket=c2wl_rocket.__main__:main",
        ]
    },
    install_requires=[
                      'PyYAML',
                      'flask>=1.0.0',
                      'flask-restful',
                      'cwltool==1.0.20180809224403',
                      "requests"         
                      ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX', 
        'Operating System :: POSIX :: Linux',    
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 8.1', 
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: System :: Distributed Computing',
    ]
)