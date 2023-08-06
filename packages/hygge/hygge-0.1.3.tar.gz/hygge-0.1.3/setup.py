# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hygge']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.5,<4.0']

setup_kwargs = {
    'name': 'hygge',
    'version': '0.1.3',
    'description': "A cozzy('hygge') way to get json response back asynchronously",
    'long_description': '.. image:: https://github.com/Proteusiq/hygge/blob/master/hygge.png\n  :target: https://github.com/Proteusiq/hygge\n\nHygge (\'Cozzy\') Response \n=========================\n\n"A cozzy(\'hygge\') way to get json response back asynchronously"\n\n.. contents:: Topics\n\nOverview\n--------\n\nIt should be easy to return json response asynchronously. hygge aim to be a fuzzy-less way to do just that.\nJust pass a url and \'get\' arguments such as params, headers, and receive back a json response. \n\nwebsite: `hygge <https://github.com/Proteusiq/hygge>`_.\n\n.. code-block:: shell-session\n\n   # install hygge\n   pip install hygge\n   \nHow to use\n\n.. code-block:: python\n\n    from hygge.get import GetResponse\n\n    url = \'https://www.trustpilot.com/businessunit/search\'\n    params = {\'country\': \'dk\', \'query\': \'mate.bike\'}\n\n    # passing url and parameters \n    res = GetResponse(url).get(params=params)\n    print(res)\n\n    # passing only url\n    info_url = f\'https://www.trustpilot.com/businessunit/{res["businessUnits"][0]["id"]}/companyinfobox\'\n    print(GetResponse(info_url).get())\n    \n',
    'author': 'Prayson Wilfred Daniel',
    'author_email': 'praysonwilfred@gmail.com',
    'url': 'https://github.com/Proteusiq/hygge',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
