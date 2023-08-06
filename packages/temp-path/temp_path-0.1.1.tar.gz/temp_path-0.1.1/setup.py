# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

modules = \
['temp_path']
setup_kwargs = {
    'name': 'temp-path',
    'version': '0.1.1',
    'description': 'A tool to temporarily add folders to the path.',
    'long_description': "# temp_path\n\nThis is a package to allow you to add a folder to the path temporarily.\n\nOften when you deal with other people's code, it's not set up to be importable /\npackaged. This tool allows you to import from those files anyways, without\nhaving to permanently modify your path.\n\nSimply run:\n\n```python\nfrom temp_path import temp_path\nwith temp_path('../someone/elses/code'):\n    import their.messy.code\n\ntheir.messy.code.use()\n```\n\nOf course, this is not just for importing python modules but also for other\nstuff you might need on your path.\n",
    'author': 'Jan Freyberg',
    'author_email': 'jan.freyberg@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
