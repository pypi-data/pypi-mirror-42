# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['psmon']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.5,<6.0']

setup_kwargs = {
    'name': 'psmon',
    'version': '0.1.0',
    'description': 'Process monitoring',
    'long_description': None,
    'author': 'Rakha Kanz Kautsar',
    'author_email': 'rkkautsar@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
