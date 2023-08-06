import numpy
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
extension = Extension(name="ufuncify_matrix_1",
                      sources=["ufuncify_matrix_1.pyx",
                               "ufuncify_matrix_1_c.c"],
                      extra_compile_args=[],
                      extra_link_args=[],
                      include_dirs=[numpy.get_include()])
setup(name="eval_matrix",
      ext_modules=cythonize([extension]))
