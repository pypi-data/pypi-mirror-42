# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['celltk',
 'celltk.labeledarray',
 'celltk.labeledarray.labeledarray',
 'celltk.utils']

package_data = \
{'': ['*']}

install_requires = \
['Cython==0.29.6',
 'PyWavelets==1.0.1',
 'SimpleITK==1.1.0',
 'backports.functools_lru_cache>=1.5,<2.0',
 'backports.weakref>=1.0,<2.0',
 'centrosome==1.0.5',
 'fast-histogram==0.5',
 'joblib==0.10.2',
 'keras==2.0.0',
 'mahotas==1.4.1',
 'matplotlib==2.1.1',
 'mock==2.0.0',
 'numba>=0.42.1,<0.43.0',
 'numpy==1.15.4',
 'opencv-python==3.2.0.7',
 'pandas==0.18.1',
 'pymorph==0.96',
 'pypng==0.0.18',
 'scikit-image==0.14.2',
 'scipy==0.19.0',
 'subprocess32>=3.5,<4.0',
 'tensorflow==1.8.0',
 'tifffile==2018.11.6']

entry_points = \
{'console_scripts': ['celltk = celltk.caller:main']}

setup_kwargs = {
    'name': 'celltk',
    'version': '0.2',
    'description': 'live-cell image analysis',
    'long_description': None,
    'author': 'Takamasa Kudo',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
