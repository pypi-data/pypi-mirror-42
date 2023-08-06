# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': '.'}

packages = \
['cscart']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'cscart-api-client',
    'version': '0.1.0',
    'description': 'CS-Cart API Client for Python and also Human',
    'long_description': '# CS-Cart API Client for Python\n\nClient for CS-Cart. wip\n\n\n## Usage\n```.py\nimport cscart\n\nclient = cscart.Client("https://storeofcscart.com", "admin@cscartstore.com", "APIKEYHOGEHOGE")\n\nres = client.get_orders()\n```\n\n## install\n```.sh\npip install cscart_api_client\n```\n',
    'author': 'Mizkino',
    'author_email': 'Mizkino@gmail.com',
    'url': 'https://github.com/Mizkino',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
