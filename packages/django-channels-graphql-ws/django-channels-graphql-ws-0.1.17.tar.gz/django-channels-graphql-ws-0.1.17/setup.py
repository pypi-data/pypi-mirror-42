# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['channels_graphql_ws']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp',
 'asgiref',
 'channels',
 'django',
 'graphene',
 'graphene_django',
 'graphql-core',
 'msgpack',
 'namedlist',
 'rx']

setup_kwargs = {
    'name': 'django-channels-graphql-ws',
    'version': '0.1.17',
    'description': 'Django Channels based WebSocket GraphQL server with Graphene-like subscriptions',
    'long_description': None,
    'author': 'Alexander A. Prokhorov',
    'author_email': 'alexander.prokhorov@datadvance.net',
    'url': 'https://github.com/datadvance/DjangoChannelsGraphqlWs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
