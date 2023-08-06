# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['timew']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8,<3.0']

setup_kwargs = {
    'name': 'timew',
    'version': '0.0.21',
    'description': 'Python bindings for your timewarrior database',
    'long_description': '# timew - Python API for Timewarrior #\n\n## Installation ##\n\nFor this API to work, you need [Timewarrior](https://taskwarrior.org/docs/timewarrior/download.html) installed\n\nInstallation is easy from the [Python Package Index](https://pypi.org/project/timew/)\n\n```bash\npip install timew\n```\n\n## API Documentation ##\n[Read the docs](http://tjaart.gitlab.io/python-timew)\n\n\n## Examples ##\n\n```bash\n>>> from timew import TimeWarrior\n\n>>> timew = TimeWarrior()\n\n>>> timew.start(time=datetime(2018, 8, 15, 9, 0, 0), tags=[\'my tag\'])\nTracking "my tag"\nStarted 2018-09-06T09:00:00\nCurrent         07T13:20:45\nTotal              28:20:45\n\n>>> timew.cancel()\nCanceled active time tracking.\n\n>>> timew.delete(1)\nDeleted @1\n\n>>> timew.join(1, 2)\nJoined @1 and @2\n\n>>> from timew import Duration\n>>> from datetime import timedelta\n>>> timew.lengthen(1, Duration(timedelta(minutes=30)))\nLengthened @1 by 0:30:00\n\n>>> timew.move(1, datetime(2018, 8, 15, 9, 0, 0))\nMoved @1 to 2018-09-05T09:00:00\n\n>>> timew.shorten(1, Duration(timedelta(minutes=10)))\nShortened @1 by 0:10:00\n\n>>> timew.split(1)\nSplit @1\n\n>>> timew.start(tags=[\'my tag\'])\nTracking "my tag"\nStarted 2018-09-07T13:37:00\nCurrent               40:22\nTotal               0:03:22\n\n>>> timew.stop()\nRecorded "my tag"\nStarted 2018-09-07T13:37:00\nEnded                 40:53\nTotal               0:03:53\n\n>>> timew.track(start_time=datetime(2018, 9, 7, 11, 0, 0), end_time=datetime(2018, 9, 7, 12, 0, 0))\nTracking "from 20180907T110000 - 20180907T120000"\nStarted 2018-09-07T13:42:27\nCurrent                  27\nTotal               0:00:00\n```\n',
    'author': 'Tjaart van der Walt',
    'author_email': 'tjaart@tjaart.org',
    'url': 'https://gitlab.com/tjaart/python-timew',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
