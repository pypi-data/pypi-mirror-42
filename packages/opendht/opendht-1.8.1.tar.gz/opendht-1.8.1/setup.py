from distutils.core import setup
from Cython.Build import cythonize

setup(name='opendht',
      version='1.8.1',
      url='https://github.com/manuels/opendht-py',
      ext_modules=cythonize("opendht.pyx"))
