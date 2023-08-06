# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['nacf']

package_data = \
{'': ['*']}

install_requires = \
['nalude>=0.2.0,<0.3.0', 'requests_html>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'nacf',
    'version': '1.0.0',
    'description': 'Nasy Crawler Framework -- Never had such a pure crawler.',
    'long_description': '# Table of Contents\n\n-   [Prologue](#org6dc9402)\n-   [Packages](#org37032fa)\n-   [Development Process](#org1eb07f9)\n    -   [Http Functions](#orgd862ea6)\n        -   [Get](#orgb88fa50)\n        -   [Post](#orgd091da7)\n        -   [Bugs](#orga99911a)\n            -   [Fix an error from inspect.Parameter which caused the function parallel down.](#orga7af803):err:1:\n    -   [Docs](#orga5017d7)\n        -   [Usage](#org21efc61)\n-   [Epoligue](#org1e897d7)\n    -   [History](#orgba8919d)\n        -   [Version 1.0.0](#orgb21403b)\n        -   [Version 0.1.2](#orgcd42135)\n        -   [Version 0.1.1](#orgce6ff7d)\n        -   [Version 0.1.0](#orgcc23226)\n\n\n\n<a id="org6dc9402"></a>\n\n# Prologue\n\nNever had such a pure crawler like this `nacf`.\n\nAlthough I often write crawlers, I don&rsquo;t like to use huge frameworks, such as scrapy, but prefer\nsimple `requests+bs4` or more general `requests_html`.  However, these two are inconvenient for a\ncrawler.  E.g. Places, such as error retrying or parallel crawling, need to be handwritten by\nmyself.  It is not very difficult to write it while writing too much can be tedious.  Hence I\nstarted writing this nacf (Nasy Crawler Framework), hoping to simplify some error retrying or\nparallel writing of crawlers.\n\n\n<a id="org37032fa"></a>\n\n# Packages\n\n<table>\n<caption class="t-above"><span class="table-number">Table 1:</span> Packages</caption>\n\n<colgroup>\n<col  class="org-left">\n\n<col  class="org-right">\n\n<col  class="org-left">\n</colgroup>\n<thead>\n<tr>\n<th scope="col" class="org-left">Package</th>\n<th scope="col" class="org-right">Version</th>\n<th scope="col" class="org-left">Description</th>\n</tr>\n</thead>\n\n<tbody>\n<tr>\n<td class="org-left">requests-html</td>\n<td class="org-right">0.9.0</td>\n<td class="org-left">HTML Parsing for Humans.</td>\n</tr>\n\n\n<tr>\n<td class="org-left">nalude</td>\n<td class="org-right">0.2.0</td>\n<td class="org-left">A standard module.  Inspired by Haskell&rsquo;s Prelude.</td>\n</tr>\n</tbody>\n</table>\n\n\n<a id="org1eb07f9"></a>\n\n# Development Process\n\n\n<a id="orgd862ea6"></a>\n\n## DONE Http Functions\n\n<p><span class="timestamp-wrapper"><span class="timestamp-kwd">CLOSED:</span> <span class="timestamp">&lt;Thu Feb 28 20:51:00 2019&gt;</span></span></p>\n\n\n<a id="orgb88fa50"></a>\n\n### DONE Get\n\n<p><span class="timestamp-wrapper"><span class="timestamp-kwd">CLOSED:</span> <span class="timestamp">&lt;Tue Dec 25 17:36:00 2018&gt;</span></span></p>\n\n\n<a id="orgd091da7"></a>\n\n### DONE Post\n\n<p><span class="timestamp-wrapper"><span class="timestamp-kwd">CLOSED:</span> <span class="timestamp">&lt;Thu Feb 28 20:44:00 2019&gt;</span></span></p>\n\n\n<a id="orga99911a"></a>\n\n### DONE Bugs\n\n<p><span class="timestamp-wrapper"><span class="timestamp-kwd">CLOSED:</span> <span class="timestamp">&lt;Thu Feb 28 20:51:00 2019&gt;</span></span></p>\n\n\n<a id="orga7af803"></a>\n\n#### DONE Fix an error from inspect.Parameter which caused the function parallel down.     :err:1:\n\n<p><span class="timestamp-wrapper"><span class="timestamp-kwd">CLOSED:</span> <span class="timestamp">&lt;Wed Dec 26 20:26:00 2018&gt;</span></span></p>\n\n\n<a id="orga5017d7"></a>\n\n## NEXT Docs\n\n\n<a id="org21efc61"></a>\n\n### NEXT Usage\n\n\n<a id="org1e897d7"></a>\n\n# Epoligue\n\n\n<a id="orgba8919d"></a>\n\n## History\n\n\n<a id="orgb21403b"></a>\n\n### Version 1.0.0\n\n-   **Data:** <span class="timestamp-wrapper"><span class="timestamp">&lt;Thu Feb 28, 2019&gt;</span></span>\n-   **Changes:** Now, old HTTP methods (`get` and `post`) cannot accept multiple URLs. Instead, we can use `gets` and `posts`.\n-   **Adds:** -   `nacf.html`\n    -   `nacf.json`\n    -   `nacf.gets`\n    -   `nacf.posts`\n-   **Includes:** -   `nalude`\n\n\n<a id="orgcd42135"></a>\n\n### Version 0.1.2\n\n-   **Data:** <span class="timestamp-wrapper"><span class="timestamp">&lt;Wed Dec 26, 2018&gt;</span></span>\n-   **Fixed:** `inspect.Parameter` error in last version.\n\n\n<a id="orgce6ff7d"></a>\n\n### Version 0.1.1\n\n-   **Data:** <span class="timestamp-wrapper"><span class="timestamp">&lt;Wed Dec 26, 2018&gt;</span></span>\n-   **Ignored:** An error caused by `inspect.Parameter`\n-   **Help Wanted:** Can someone help me about the Parameter?\n\n\n<a id="orgcc23226"></a>\n\n### Version 0.1.0\n\n-   **Date:** <span class="timestamp-wrapper"><span class="timestamp">&lt;Sun Dec 23, 2018&gt;</span></span>\n-   **Commemorate Version:** First Version\n    -   Basic Functions.\n',
    'author': 'Nasy',
    'author_email': 'nasyxx+nacf@gmail.com',
    'url': 'https://github.com/nasyxx/nacf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
