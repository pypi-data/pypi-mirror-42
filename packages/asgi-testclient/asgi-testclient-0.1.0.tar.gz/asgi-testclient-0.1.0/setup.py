# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['asgi_testclient']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asgi-testclient',
    'version': '0.1.0',
    'description': 'Test Clietn for ASGI web applications',
    'long_description': '# asgi-testClient\n![Travis (.org)](https://img.shields.io/travis/oldani/asgi-testClient.svg)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/asgi-testClient.svg)\n![PyPI](https://img.shields.io/pypi/v/asgi-testClient.svg)\n[![codecov](https://codecov.io/gh/oldani/asgi-testClient/branch/master/graph/badge.svg)](https://codecov.io/gh/oldani/asgi-testClient)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/asgi-testClient.svg)\n[![black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/ambv/black)\n\nTesting ASGI applications made easy!\n\n\n## The why?\n\n**Why** would you build this when all web frameworks come with one? Well, because mostly all those web frameworks have to build their own. I was building my own web framework perhaps (research & learning purpose) and got to the point where a needed a `TestClient` but then a asked my self **why does anybody building web frameworks have to build their own TestClient when there\'s a standard?**. Ok, then just install `starlette` a use it test client; would you install a library just to use a tiny part of it? **This client does not have any dependencies**.\n\n## Requirements\n\n`Python 3.6+`\n\nIt should run on Python 3.5 but I haven\' tested it.\n\n## Installation\n\n`pip install asgi-testclient`\n\n\n## Usage\n\nThe client replicates the requests API, so if you have used request you should feel comfortable.\n\n```python\nimport pytest\nfrom asgi_testclient import TestClient\n\nfrom myapp import API\n\n@pytest.fixture\ndef client():\n    return TestClient(API)\n\n\n@pytest.mark.asyncio\nasync def test_get(client):\n    response = await client.get("/")\n    assert response.json() == {"hello": "world"}\n    assert response.status_code == 200\n```\n\nI have used `pytest` in this example but you can use whichever runner you prefer. *Note:* the client method are coroutines `get, post, delete, put, patch, etc..`.\n\n## TODO:\n- [ ] Support Websockets client.\n- [ ] Cookies support.\n- [ ] Redirects.\n- [ ] Support files encoding\n- [ ] Stream request & response\n\n\n## Credits\n\n- `Tom Christie`: I brought inspiration from the `starlette` test client.\n- `Kenneth ☤ Reitz`: This package tries to replicate `requests` API.',
    'author': 'Ordanis Sanchez',
    'author_email': 'ordanisanchez@gmail.com',
    'url': 'https://github.com/oldani/asgi-testClient',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
