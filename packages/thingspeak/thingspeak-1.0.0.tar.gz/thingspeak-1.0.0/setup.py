# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['thingspeak']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'requests>=2.21,<3.0']

entry_points = \
{'console_scripts': ['thingspeak = thingspeak.cmdline:main']}

setup_kwargs = {
    'name': 'thingspeak',
    'version': '1.0.0',
    'description': 'Client library for the thingspeak.com API',
    'long_description': 'Client library for the thingspeak.com API\n=========================================\n\n|saythanks| master: |masterbadge| develop: |developbadge|\n\n.. |masterbadge| image:: https://travis-ci.org/mchwalisz/thingspeak.svg?branch=master\n    :target: https://travis-ci.org/mchwalisz/thingspeak\n\n.. |developbadge| image:: https://travis-ci.org/mchwalisz/thingspeak.svg?branch=develop\n    :target: https://travis-ci.org/mchwalisz/thingspeak\n\n.. |saythanks| image:: https://img.shields.io/badge/SayThanks.io-%E2%98%BC-1EAEDB.svg\n    :target: https://saythanks.io/to/mchwalisz\n    :alt: Say thanks!\n\nThingSpeak is an open source “Internet of Things” application and API to store and retrieve data from things using HTTP over the Internet or via a Local Area Network. With ThingSpeak, you can create sensor logging applications, location tracking applications, and a social network of things with status updates. https://thingspeak.com https://github.com/iobridge/ThingSpeak\n\nThis repository is contains Python module that helps in talking to ThingSpeak API.\n\nFull documentation is under http://thingspeak.readthedocs.io/en/latest/\n\nInstall using::\n\n    pip install thingspeak\n\n.. warning::\n\n   This is a complete redesign of the library as compared to v0.1.1.\n   Previous version is available in https://github.com/bergey/thingspeak\n   and is no longer maintained.\n\n   To install old version you can still use::\n\n      pip install thingspeak==0.1.1\n',
    'author': 'Mikołaj Chwalisz',
    'author_email': 'm.chwalisz@gmail.com',
    'url': 'https://thingspeak.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
