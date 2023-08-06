# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['kirlent_sphinx']

package_data = \
{'': ['*'],
 'kirlent_sphinx': ['templates/kirlent/kirlent-tailwind.css',
                    'templates/kirlent/kirlent-tailwind.css',
                    'templates/kirlent/kirlent-tailwind.css',
                    'templates/kirlent/kirlent-tailwind.css',
                    'templates/kirlent/layout.html',
                    'templates/kirlent/layout.html',
                    'templates/kirlent/layout.html',
                    'templates/kirlent/layout.html',
                    'templates/kirlent/static/*',
                    'templates/kirlent/static/css/*',
                    'templates/kirlent/static/css/print/*',
                    'templates/kirlent/static/css/theme/*',
                    'templates/kirlent/static/css/theme/source/*',
                    'templates/kirlent/static/css/theme/template/*',
                    'templates/kirlent/static/js/*',
                    'templates/kirlent/static/lib/js/*',
                    'templates/kirlent/static/plugin/markdown/*',
                    'templates/kirlent/static/plugin/multiplex/*',
                    'templates/kirlent/static/plugin/notes-server/*',
                    'templates/kirlent/static/plugin/notes/*',
                    'templates/kirlent/static/plugin/print-pdf/*',
                    'templates/kirlent/static/plugin/zoom-js/*',
                    'templates/kirlent/tailwind.js',
                    'templates/kirlent/tailwind.js',
                    'templates/kirlent/tailwind.js',
                    'templates/kirlent/tailwind.js',
                    'templates/kirlent/theme.conf',
                    'templates/kirlent/theme.conf',
                    'templates/kirlent/theme.conf',
                    'templates/kirlent/theme.conf']}

install_requires = \
['sphinx>=1.8,<2.0']

setup_kwargs = {
    'name': 'kirlent-sphinx',
    'version': '0.2.0',
    'description': 'Sphinx extension for slides and extended tables.',
    'long_description': 'kirlent_sphinx is a Sphinx extension that is primarily meant to be used with\nthe `Kırlent`_ educational content management system, although it can be used\nas a regular Sphinx extension.\n\nFeatures\n--------\n\nkirlent_sphinx provides the following components:\n\n- An extended ``table`` directive derived from the `Cloud Sphinx Theme`_\n  project.\n\n- A ``slide`` directive and a corresponding HTML theme based on `RevealJS`_,\n  derived from the `sphinxjp.themes.revealjs`_ project.\n\nGetting started\n---------------\n\nYou can install kirlent_sphinx with pip::\n\n  pip install kirlent_sphinx\n\nTo enable it in your project, make the following changes in ``conf.py``:\n\n- Add ``kirlent_sphinx`` to extensions::\n\n    extensions = ["kirlent_sphinx"]\n\n- Set ``kirlent`` as the theme::\n\n    html_theme = "kirlent"\n\n- Disable index generation::\n\n    html_use_index = False\n\nUsage\n-----\n\nFor the extended ``table`` directive, consult the documentation\nof the `table_styling`_ extension of the `Cloud Sphinx Theme`_ project.\n\nThe ``slide`` and ``speaker-notes`` directives are derived from the\n``revealjs`` and ``rv_note`` directives of the `sphinxjp.themes.revealjs`_\nproject. The ``rv_small`` and ``rv_code`` directives of that project have been\nremoved.\n\nThe Kırlent HTML theme uses pygments for code highlighting instead of\nhighlight.js which is used by the original theme. In addition, it uses\n`Tailwind`_ utility classes for styling:\n\n  .. slide:: Slide title\n\n     .. container:: columns\n\n        .. container:: column w-1/3 bg-blue-lighter\n\n           - item 1a\n           - item 1b\n\n        .. container:: column bg-red-lighter\n\n           - item 2\n\n     .. speaker-notes::\n\n        some extra explanation\n\nLicense\n-------\n\nCopyright (C) 2019 H. Turgut Uyar <uyar@tekir.org>\n\nkirlent_sphinx is released under the BSD license. Read the included\n``LICENSE.txt`` file for details.\n\nkirlent_sphinx contains code derived from the `Cloud Sphinx Theme`_ project\nwhich is released under the BSD license. Read the included\n``LICENSE_cloud_spheme.txt`` file for details.\n\nkirlent_sphinx contains code derived from the `sphinxjp.themes.revealjs`_\nproject which is released under the MIT license. Read the included\n``LICENSE_sphinxjp.themes.revealjs.txt`` file for details.\n\nkirlent_sphinx contains code from the `RevealJS`_ project which is\nreleased under the MIT license. Read the included ``LICENSE_revealjs.txt``\nfile for details.\n\nkirlent_sphinx contains code from the `Tailwind`_ project which is\nreleased under the MIT license. Read the included ``LICENSE_tailwind.txt``\nfile for details.\n\n.. _Kırlent: https://gitlab.com/tekir/kirlent/\n.. _Cloud Sphinx Theme: https://cloud-sptheme.readthedocs.io/en/latest/\n.. _table_styling: https://cloud-sptheme.readthedocs.io/en/latest/lib/cloud_sptheme.ext.table_styling.html\n.. _sphinxjp.themes.revealjs: https://github.com/tell-k/sphinxjp.themes.revealjs\n.. _RevealJS: https://revealjs.com/\n.. _Tailwind: https://tailwindcss.com/\n',
    'author': 'H. Turgut Uyar',
    'author_email': 'uyar@tekir.org',
    'url': 'https://gitlab.com/tekir/kirlent_sphinx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
