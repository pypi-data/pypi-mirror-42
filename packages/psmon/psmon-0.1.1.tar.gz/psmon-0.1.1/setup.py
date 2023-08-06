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
    'version': '0.1.1',
    'description': 'Process monitoring',
    'long_description': '# psmon\n\nMonitors and limits process resource\n',
    'author': 'Rakha Kanz Kautsar',
    'author_email': 'rkkautsar@gmail.com',
    'url': 'https://github.com/rkkautsar/psmon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
