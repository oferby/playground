from setuptools import setup, find_packages
import io
import os

here = os.path.abspath(os.path.dirname(__file__))
from distutils.core import setup

setup(name='vca',
      classifiers=[
          "Development Status :: 1 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Apache Software License",
          # supported python versions
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.6",
          "Topic :: Software Development :: Libraries",
      ],
      version='1.0',
      description='Virtual Cloud Assistant',
      author='Ofer Ben-Yacov',
      author_email='ofer.benyacov@huawei.com',
      packages=['vca', ],
      )
