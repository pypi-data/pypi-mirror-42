# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['papermill_sftp']

package_data = \
{'': ['*']}

install_requires = \
['pysftp>=0.2.9,<0.3.0']

setup_kwargs = {
    'name': 'papermill-sftp',
    'version': '0.0.1',
    'description': 'A papermill SFTP I/O handler.',
    'long_description': '# papermill_sftp\n\nA library to act as an SFTP interface for the papermill library.\n\nOnce installed, you can run:\n\n```bash\npapermill sftp://my.sftp.server/my-notebook.ipynb sftp://my.sftp.server/output.ipynb\n```\n',
    'author': 'Jan Freyberg',
    'author_email': 'jan.freyberg@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
