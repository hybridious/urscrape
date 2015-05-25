#!/usr/bin/python3
# -*-python-*-
'''
Copyright 2015 Pham Urwen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import lxml.html
import os
import sys

# Make sure the urscrape and configuration files are in the path
bindir = os.path.dirname(os.path.abspath(__file__))
pbindir = os.path.dirname(bindir)
if bindir not in sys.path:
    sys.path.insert(1, bindir)
if pbindir not in sys.path:
    sys.path.insert(1, pbindir)

from urscrape import urparse

html = '''
<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank updated="yes">2</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank updated="yes">5</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
</data>
<body>
<div class='foo'>
<t1><b>text1</b></t1>textt2
<t1><b>text3</b></t1>textt4
</div>
</body>
'''

rules = '''
body div text()
'''

up = urparse.UrParse()
up.load(rules)
up.print_rules()

tree = lxml.html.fromstring(html)
for el in tree.iter():
  print(el.tag)
