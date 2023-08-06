from setuptools import setup
import catscii.catscii as cats

setup(
   name = 'catscii',
   version = cats.__version__,
   author = cats.__credits__,
   packages = ['catscii'],
   description = 'A simple catalog query tool in python',
   python_requires = '>=3.6',
   install_requires = [
       "numpy >= 1.16",
   ],
   include_package_data=True,
)
