from setuptools import setup, find_packages
from os import path
setup(
   name="rzn",
   version='0',
   description="rzn - rsync/rclone git like push/pull wrapper",
   packages=find_packages(exclude=[]),
   entry_points={
       "console_scripts": [
           "rzn=rzn.rzn:main",
       ]
   },
)
