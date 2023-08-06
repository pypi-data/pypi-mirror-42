# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['crucyble']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'crucyble',
    'version': '0.1.0.dev1',
    'description': 'A Cython Wrapped GloVe',
    'long_description': '# crucyble\n\nA **Cy**thon Wrapped GloVe (Global Vectors for Word Representation)\n\n> *crucible*, noun. \n>\n> **Pronounciation**: \\ ˈkrü-sə-bəl \\\n> 1. a vessel of a very refractory material used for melting...\n> 2. a severe test\n> 3. a vessel of a very refractory (see refractory entry 1 sense 3) material (such as porcelain) used for melting and calcining a substance that requires a   high degree of heat\n>\n> **Synonyms**: gauntlet, ...\n\n## Overview\n\nThis library aims to provide the GloVe algorithm in a nearly-unaltered format relative to its original distribution by stanfordnlp.\n\nThe bulk of the alterations consist of removing the `main()` methods from the glove applications, and converting them to accept filenames instead of stdin/stdout. (See pull requests [1](https://github.com/ttymck/crucyble/pull/1), [2](https://github.com/ttymck/crucyble/pull/2), and [3](https://github.com/ttymck/crucyble/pull/3))\n\nThese altered C sources are then wrapped with Cython to provide "native extensions" in the Python runtime.\n\n## Development\n\n### Local Testing\n**Prerequisites**: `gcc` and [cython](https://cython.readthedocs.io/en/latest/src/quickstart/install.html) installed.\n\nTo test this library locally:\n1. clone the repo\n2. from `crucyble/` run `python setup.py build_ext -i`\n3. try: `PYTHONPATH=. python test/test_glove.py`\n4. examine the outputs!\n\nYou can change the corpus variable in `test_glove.py` to point to any corpus you have locally.\n\n### Contributing\n...coming soon\n\n## Performance\n\nTodo... :shrug:\n\n## License Info\n\nDerivative implementation of the [GloVe library from Stanford](https://github.com/stanfordnlp/GloVe) redistributed in accordance with [Apache License](./src/lib/glove/LICENSE) and redistributed under [MIT License](./LICENSE)',
    'author': 'Tyler Kontra',
    'author_email': 'tyler@tylerkontra.com',
    'url': 'https://github.com/ttymck/crucyble',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
