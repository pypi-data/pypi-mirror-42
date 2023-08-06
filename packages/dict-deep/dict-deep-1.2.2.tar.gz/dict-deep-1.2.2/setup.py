# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dict_deep']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dict-deep',
    'version': '1.2.2',
    'description': "Very simple deep_set and deep_get functions to access nested dicts using 'dotted strings' as key.",
    'long_description': '## Description\n\nSimple functions to set or get values from a nested dict structure\n\nThis module DOES NOT implement dotted notation as an alternative access method for dicts.\nI generally do not like changing python dicts to enable dot notation, hence no available\npackage fitted my needs for a simple deep accessor.\n\n\n## Arguments\n\n*deep_get* accepts:\n- d: the dictionary\n- key: a string OR anything accepted by the list() constructor\n- access_method: one of METHOD_ATTR (assumed if default is None), METHOD_GET,\n                 METHOD_SETDEFAULT (assumed if default is not None). This determines the method\n                 to be used to access the nested dict structure. \n- default: a callable to be used as default for the dict .get or .setdefault functions\n- sep: by default it is a dot \'.\', you can use anything the string function split will accept\n\n\n*deep_set* accepts:\n- d: same as above\n- key: same as above\n- value\n- default: if set (not None which is the default), will use setdefault to traverse the nested dict structure\n- sep: same as above\n\n\n*deep_del* accepts:\n- d: same as above\n- key: same as above\n- sep: same as above\n\nIt returns a tuple:\n(True, <value of the entry that was deleted>) or\n(False, None)\n\n## How to use\n\n    from dict_deep import deep_get, deep_set, deep_del\n    \n    \n    i = 0\n    \n    # Alternative 1\n    i += 1\n    d = {\'a\': {\'b\': {}}}\n    deep_set(d, "a.b.c", "Hello World")\n    print("{}: {}".format(i, deep_get(d, "a.b.c")))\n    \n    # Alternative 2\n    i += 1\n    d = {}\n    deep_set(d, [\'a\', \'b\', \'c\'], "Hello World", default=lambda: dict())\n    print("{}: {}".format(i, deep_get(d, "a.b.c")))\n    \n    # Alternative 3\n    i += 1\n    d = {}\n    deep_set(d, "a->b->c", "Hello World", default=lambda: dict(), sep="->")\n    print("{}: {}".format(i, deep_get(d, "a->b->c", sep="->")))\n    \n    # Alternative 4\n    i += 1\n    d = {}\n    _ = deep_get(d=d, key=[\'a\', \'b\'], default=lambda: dict(), sep=".")\n    _[\'c\'] = "Hello World"\n    print("{}: {}".format(i, deep_get(d, "a.b.c")))\n    \n    # deep_del\n    i += 1\n    d = {}\n    deep_set(d, "1.1.1", \'a\', default=lambda: dict())\n    deep_set(d, "1.1.2", \'Hello World\')\n    deep_set(d, "1.1.3", \'c\')\n    print("{}: {}".format(i, deep_del(d, "1.1.2")[1]))\n',
    'author': 'mbello',
    'author_email': 'mbello@users.noreply.github.com',
    'url': 'https://github.com/mbello/dict-deep',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
