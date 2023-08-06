# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['nautc']
install_requires = \
['requests>=2.21,<3.0']

entry_points = \
{'console_scripts': ['nautc = nautc:main']}

setup_kwargs = {
    'name': 'nautc',
    'version': '0.1.0',
    'description': '<http://qaz.wtf/u/convert.cgi?text=nautc> Convert plain text (letters, sometimes numbers, sometimes punctuation) to obscure characters from Unicode.',
    'long_description': None,
    'author': 'Nasy',
    'author_email': 'nasyxx+python@gmail.com',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
