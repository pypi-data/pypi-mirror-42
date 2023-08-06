# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pynetrees']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.10.1,<0.11.0',
 'matplotlib>=3.0,<4.0',
 'pandas==0.23.4',
 'seaborn>=0.9.0,<0.10.0']

extras_require = \
{'examples': ['jupyter>=1.0,<2.0']}

setup_kwargs = {
    'name': 'pynetrees',
    'version': '1.0.1',
    'description': 'Tools to work with decision trees',
    'long_description': None,
    'author': 'François Trahan',
    'author_email': 'francois.trahan@gmail.com',
    'url': 'https://github.com/francoistrahan/pynes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
