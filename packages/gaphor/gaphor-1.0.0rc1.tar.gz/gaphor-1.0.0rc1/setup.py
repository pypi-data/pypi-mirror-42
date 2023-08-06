# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gaphor',
 'gaphor.UML',
 'gaphor.UML.tests',
 'gaphor.adapters',
 'gaphor.adapters.actions',
 'gaphor.adapters.actions.tests',
 'gaphor.adapters.classes',
 'gaphor.adapters.classes.tests',
 'gaphor.adapters.components',
 'gaphor.adapters.components.tests',
 'gaphor.adapters.interactions',
 'gaphor.adapters.interactions.tests',
 'gaphor.adapters.profiles',
 'gaphor.adapters.profiles.tests',
 'gaphor.adapters.states',
 'gaphor.adapters.states.tests',
 'gaphor.adapters.tests',
 'gaphor.adapters.usecases',
 'gaphor.adapters.usecases.tests',
 'gaphor.diagram',
 'gaphor.diagram.actions',
 'gaphor.diagram.classes',
 'gaphor.diagram.classes.tests',
 'gaphor.diagram.components',
 'gaphor.diagram.components.tests',
 'gaphor.diagram.profiles',
 'gaphor.diagram.states',
 'gaphor.diagram.states.tests',
 'gaphor.diagram.tests',
 'gaphor.misc',
 'gaphor.plugins',
 'gaphor.plugins.alignment',
 'gaphor.plugins.checkmetamodel',
 'gaphor.plugins.diagramlayout',
 'gaphor.plugins.diagramlayout.tests',
 'gaphor.plugins.liveobjectbrowser',
 'gaphor.plugins.pynsource',
 'gaphor.plugins.xmiexport',
 'gaphor.services',
 'gaphor.services.tests',
 'gaphor.storage',
 'gaphor.storage.tests',
 'gaphor.tests',
 'gaphor.tools',
 'gaphor.ui',
 'gaphor.ui.pixmaps',
 'gaphor.ui.tests']

package_data = \
{'': ['*'], 'gaphor.diagram.actions': ['tests/*'], 'gaphor.misc': ['tests/*']}

install_requires = \
['PyGObject>=3.30,<4.0',
 'gaphas>=1.0.0,<2.0.0',
 'pycairo>=1.18,<2.0',
 'zope.component>=4.5,<5.0']

setup_kwargs = {
    'name': 'gaphor',
    'version': '1.0.0rc1',
    'description': 'Gaphor is a UML modeling tool',
    'long_description': "\nGaphor\n======\n\nThe UML modeling tool.\n\n|build| |license| |pypi| |downloads| |code style|\n\n.. NOTE::\n   The latest release of Gaphor (0.17.2) uses Python 2.x and PyGTK. The master version is using Python 3.x and PyGobject (GObject-introspection).\n   Since a 1.0 version of Gaphas (the canvas component) has been released lately, also requiring PyGObject and not PyGTK, the 1.0 version of Gaphas\n   is incompatible with Gaphor 0.17.2.\n\n   Therefore, when installing Gaphor via pip, Gaphas must be pinned to version 0.7.2 with::\n\n      $ python2 -m pip install -I gaphas==0.7.2\n\n   If a newer version is already installed in your environment, make sure to uninstall Gaphas again before pinning the version.\n\nPrerequisites\n~~~~~~~~~~~~~\n\nMinimum requirements\n^^^^^^^^^^^^^^^^^^^^\n\nThis is the software that should be present on your system prior to installing Gaphor.\n\n* Python 3.x (Python 2 is not supported!)\n* GTK+3 and GObject-introspection\n\nIf you're on Linux, you will soon need to have GTK+ 3.10 or later. This is the version\nthat ships starting with Ubuntu 14.04 and Fedora 20. You will also soon need to install\nthe Python 3 bindings to GTK+.\n\nIf you're on macOS, you will soon need to be on 10.7 (Lion) or newer.\nGTK+3 and GObject-introspection should be installed with `Homebrew`_::\n\n    $ brew install gobject-introspection gtk+3\n\nWe're working on Windows support.\n\nQuickstart\n~~~~~~~~~~\n\nThe easiest way to get started is to set up a project specific Virtual Environment::\n\n    $ source ./venv\n    $ gaphor\n\nDocumentation\n~~~~~~~~~~~~~\n\nDocumentation for Gaphor can be found on `Read The Docs`_.\n\nCommunity\n~~~~~~~~~\n\nYou can talk to the community through:\n\n* The `gaphor`_ channel on Gitter.\n\nContributing\n~~~~~~~~~~~~\n\nIf you experience problems with Gaphor, `log them on GitHub`_. If you\nwant to contribute code, please `fork the code`_ and `submit a pull request`_.\n\n.. _Read The Docs: https://gaphor.readthedocs.io\n.. _gaphor: https://gitter.im/gaphor/Lobby\n.. _log them on Github: https://github.com/gaphor/gaphor/issues\n.. _fork the code: https://github.com/gaphor/gaphor\n.. _submit a pull request: https://github.com/gaphor/gaphor/pulls\n.. _Homebrew: https://brew.sh\n.. |build| image:: https://travis-ci.com/gaphor/gaphor.svg?branch=master\n    :target: https://travis-ci.com/gaphor/gaphor\n.. |license| image:: https://img.shields.io/pypi/l/gaphor.svg\n    :target: https://github.com/gaphor/gaphor/blob/master/LICENSE.txt\n.. |pypi| image:: https://img.shields.io/pypi/v/gaphor.svg\n    :target: https://pypi.org/project/gaphor/\n.. |downloads| image:: https://pepy.tech/badge/gaphor\n    :target: https://pepy.tech/project/gaphor\n.. |code style| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n",
    'author': 'Arjan J. Molenaar',
    'author_email': 'gaphor@gmail.com',
    'url': 'https://gaphor.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
