# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['get_cert']
install_requires = \
['click>=7.0,<8.0']

setup_kwargs = {
    'name': 'get-cert',
    'version': '19.1.0',
    'description': 'Tool for downloading ssl certificates from remote servers.',
    'long_description': None,
    'author': 'Michal Mazurek',
    'author_email': 'michal@mazurek-inc.co.uk',
    'url': 'https://github.com/michalmazurek/get_cert',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
