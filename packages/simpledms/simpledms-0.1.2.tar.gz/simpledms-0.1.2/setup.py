# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['simpledms', 'simpledms.ui']

package_data = \
{'': ['*'], 'simpledms.ui': ['icons/*']}

install_requires = \
['dateparser>=0.7.1,<0.8.0',
 'opencv-contrib-python>=4.0,<5.0',
 'pdfminer3>=2018.12,<2019.0',
 'pdfrw>=0.4.0,<0.5.0',
 'pypdf2>=1.26,<2.0',
 'pyqt5-sip>=4.19,<5.0',
 'pyqt5>=5.11,<6.0',
 'python-dateutil>=2.8,<3.0',
 'python-magic>=0.4.15,<0.5.0',
 'qdarkstyle>=2.6,<3.0',
 'qtmodern>=0.1.4,<0.2.0',
 'tika>=1.19,<2.0',
 'wand>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'simpledms',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
