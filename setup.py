from distutils.core import setup, Extension

module1 = Extension('_pyepanet2', sources=['pyepanet2_wrap.c',],
                runtime_library_dirs=['/usr/local/lib'],
                library_dirs=['/usr/local/lib'],
                libraries=['epanet2',])

setup (name = 'pyepanet2',
version = '1.0',
description = 'pyepanet2 wrapper library',
py_modules = ['epanet2.pyepanet2', 'pyepanet2_igraph.pyepanet2_igraph'],
ext_modules = [module1],
)

