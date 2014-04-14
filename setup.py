from distutils.core import setup, Extension

module1 = Extension('_epanet2', sources=['epanet2/epanet2_wrap.c',],
                runtime_library_dirs=['/usr/local/lib'],
                library_dirs=['/usr/local/lib'],
                libraries=['epanet2',])

setup (name = 'pyepanet2',
version = '1.0',
description = 'pyepanet2 wrapper library',
py_modules = ['epanet2.epanet2', 'epanet2.pyepanet2', 'epanet2.epa_igraph'],
ext_package='epanet2',
ext_modules = [module1],
)

