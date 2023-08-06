# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['khaki']

package_data = \
{'': ['*']}

install_requires = \
['pyglet>=1.3.2,<2.0.0']

entry_points = \
{'console_scripts': ['khaki = khaki.__main__:run']}

setup_kwargs = {
    'name': 'khaki',
    'version': '0.3.2',
    'description': 'A simple Pomodoro timer using curses (and pyglet for audio playback)',
    'long_description': 'Khaki\n=====\n\nKhaki is a Pomodoro timer in Python using the standard `curses` module and\nPyglet.\n\nHow to use\n----------\n\nRun `khaki`. Once it is running, use `p` to toggle the timer. After the\nlong timer runs out, it is replaced by the rest timer, which needs to be\ntoggled as well.\n\nPressing `+` will reset the current timer and add one second to the max\ntime. Pressing `-` works the same way, but subtracts a second. The\nchanges are not yet persistent.\n\nPressing `c` will clear the timer. It will keep running if it was running,\nand will continue paused if it was paused.\n\nYou can exit with `q`.\n\nWhy "Khaki"\n-----------\n\nIt has a nice sound to it, and a Khaki is a great doppelganger for a tomato.\n',
    'author': 'Tarcisio Eduardo Moreira Crocomo',
    'author_email': 'tarcisioe@pm.me',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
