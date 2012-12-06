from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy

extensions = [
    Extension("flame", ["flame.pyx"], )
]

setup(name="flame",
      ext_modules=extensions,
      cmdclass={"build_ext": build_ext},
      include_dirs=[numpy.get_include(), ])
