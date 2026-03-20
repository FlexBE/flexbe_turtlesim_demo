#!/usr/bin/env python

"""behaviors package setup."""

from setuptools import setup

PACKAGE_NAME = 'flexbe_turtlesim_demo_flexbe_behaviors'

setup(
    name=PACKAGE_NAME,
    version='1.3.1',
    packages=[PACKAGE_NAME],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + PACKAGE_NAME]),
        ('share/' + PACKAGE_NAME, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='David Conner',
    maintainer_email='robotics@cnu.edu',
    description='flexbe_turtlesim_demo_flexbe_behaviors provides a collection of custom '
                'behaviors to provide a simple demonstration of FlexBE using the ROS Turtlesim packages.',
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turn_rate = flexbe_turtlesim_demo_flexbe_behaviors.turn_rate:turn_rate'
        ],
    },
)
