from setuptools import setup
import catmatch.__main__ as cats

setup(
   name = 'catmatch',
   version = cats.__version__,
   author = cats.__credits__,
   packages = ['catmatch'],
   entry_points = {'gui_scripts': ['catmatch = catmatch.__main__:main',],},
   description = 'A simple catalog matching script',
   python_requires = '>=3.6',
   install_requires = [
       "numpy >= 1.16",
       "catscii>= 1.1",
   ],
   include_package_data=True,
)
