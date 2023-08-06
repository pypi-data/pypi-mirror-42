# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['transformer', 'transformer.plugins']

package_data = \
{'': ['*']}

install_requires = \
['chevron>=0.13,<0.14',
 'docopt>=0.6.2,<0.7.0',
 'ecological>=1.6,<2.0',
 'pendulum>=2.0,<3.0']

entry_points = \
{'console_scripts': ['transformer = transformer.cli:script_entrypoint']}

setup_kwargs = {
    'name': 'har-transformer',
    'version': '1.0.2.dev20190221115430',
    'description': 'A tool to convert HAR files into a locustfile.',
    'long_description': '<p align="center">\n<img src="images/transformer.png"/>\n<br>\n<a href="https://travis-ci.org/zalando-incubator/Transformer"><img src="https://travis-ci.org/zalando-incubator/Transformer.svg?branch=master"/></a>\n<a href="https://www.codacy.com/app/thilp/Transformer"><img src="https://api.codacy.com/project/badge/Grade/10b3feb4e4814429bf288b87443a6c72"/></a>\n<a href="https://www.codacy.com/app/thilp/Transformer"><img src="https://api.codacy.com/project/badge/Coverage/10b3feb4e4814429bf288b87443a6c72"/></a>\n</p>\n\n# Transformer\n\nA tool to convert web browser sessions ([HAR files][]) into\n[Locust][] load testing scenarios (locustfiles).\n\nUse it when you want to **replay HAR files** (containing recordings of\ninteractions with your website) **in load tests with Locust**.\n\n[HAR files]: https://en.wikipedia.org/wiki/.har\n[Locust]: https://locust.io/\n\n<!-- toc -->\n\n- [Installation](#installation)\n- [Usage](#usage)\n  * [Command-line](#command-line)\n  * [Library](#library)\n- [Documentation](#documentation)\n- [Authors](#authors)\n- [License](#license)\n\n<!-- tocstop -->\n\n## Installation\n\nInstall from PyPI with pip:\n\n```bash\npip install har-transformer\n```\n\n## Usage\n\n### Command-line\n\n```bash\n$ transformer my_scenarios_dir/\n```\n\n### Library\n\n```python\nimport transformer\n\nwith open("locustfile.py", "w") as f:\n    transformer.dump(f, ["my_scenarios_dir/"])\n```\n\nExample HAR files are included in the `examples` directory for you to try out.\n\n## Documentation\n\nTake a look at our **[user documentation][doc]** for more details, including\nhow to generate HAR files, customize your scenarios, use or write plugins …\n\n[doc]: https://github.com/zalando-incubator/transformer/wiki\n\n## Authors\n\n* **Serhii Cherniavskyi** - [@scherniavsky](https://github.com/scherniavsky)\n* **Thibaut Le Page** - [@thilp](https://github.com/thilp)\n* **Brian Maher** - [@bmaher](https://github.com/bmaher)\n* **Oliwia Zaremba** - [@tortila](https://github.com/tortila)\n\nSee also the list of [contributors](CONTRIBUTORS.md) who participated in this project.\n\n## License\n\nThis project is licensed under the MIT License - see the\n[LICENSE.md](LICENSE.md) file for details.\n',
    'author': 'Serhii Cherniavskyi',
    'author_email': 'serhii.cherniavskyi@zalando.de',
    'url': 'https://github.com/zalando-incubator/transformer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
