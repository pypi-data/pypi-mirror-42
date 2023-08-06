# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pycustomcfn']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2018.11,<2019.0',
 'pyrandomtools>=0.1.2,<0.2.0',
 'pysimplelogger>=0.1.2,<0.2.0',
 'urllib3>=1.24,<2.0']

setup_kwargs = {
    'name': 'pycustomcfn',
    'version': '0.1.3',
    'description': 'Module for handling dispatch and response for a CustomCFN Lambda',
    'long_description': None,
    'author': 'Rick Alm',
    'author_email': 'rick.alm@washpost.com',
    'url': 'http://github.com/wpmedia/pycustomcfn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
