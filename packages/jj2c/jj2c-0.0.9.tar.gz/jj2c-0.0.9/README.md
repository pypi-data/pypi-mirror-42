jj2c
===============================

version number: 0.0.9
author: Tom Tang

Overview
--------

Jinja2 compiler

Installation / Usage
--------------------

To install use pip:

    $ pip install jj2c


To use it:

Render from folder to folder:
    `jj2c template_folder/ -V 'a: AAA' 'b: BBB' -o output_folder/`

Render from zip to folder:
    `jj2c template.zip -V 'a: AAA' 'b: BBB' -o output_folder/`

Render from zip to zip:
    `jj2c template.zip -V 'a: AAA' 'b: BBB' -o template.zip`

Render to stdout:
    `jj2c template-file -V 'a: AAA' 'b: BBB'`

Or clone the repo:

    $ git clone https://github.com/tly1980/jj2c.git
    $ python setup.py install


Using Jinja2 extendsions
------------------------

If you wish to use jinja2 extensions, use `-e` or `--extensions` tags.

```
jj2c -e jinja2.ext.do ' '
```


Contributing
------------

TBD

Example
-------

TBD
