# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

modules = \
['temp_path']
setup_kwargs = {
    'name': 'temp-path',
    'version': '0.1.0',
    'description': 'A tool to temporarily add folders to the path.',
    'long_description': None,
    'author': 'Jan Freyberg',
    'author_email': 'jan.freyberg@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
