#!/usr/bin/env python

"""Setup for package."""

from glob import glob

from setuptools import setup
from setuptools import find_packages

PACKAGE_NAME = 'flexbe_turtlesim_demo_flexbe_states'

setup(
    name=PACKAGE_NAME,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + PACKAGE_NAME]),
        ('share/' + PACKAGE_NAME, ['package.xml']),
        ('share/' + PACKAGE_NAME + "/tests", glob('tests/*.test')),
        ('share/' + PACKAGE_NAME + "/launch", glob('tests/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='David Conner',
    maintainer_email='robotics@cnu.edu',
    description='flexbe_turtlesim_demo_flexbe_states provides a collection of custom states '
                'to provide a simple demonstration of FlexBE using the ROS Turtlesim packages.',
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
