# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mattes_dada']

package_data = \
{'': ['*']}

install_requires = \
['markovify>=0.7.1,<0.8.0', 'nltk>=3.4,<4.0', 'regex>=2019.2,<2020.0']

entry_points = \
{'console_scripts': ['mdada = mattes_dada.cmd:main']}

setup_kwargs = {
    'name': 'mattes-dada',
    'version': '0.1.0',
    'description': 'Semi-random text generator using Markov chains',
    'long_description': "Matte's Dada\n===\n\nSemi-random text generator using Markov chains\n\nRun\n==\n\n```shell\nmdada input_file\n```\n\nwhere input_file is a path to either a txt ot odt file\n",
    'author': 'Raphael Krupinski',
    'author_email': None,
    'url': 'https://github.com/mattesilver/dada',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
