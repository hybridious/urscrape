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

from urscrape import urhtml
from urscrape import urlogging
import re
import shlex

class UrParse(urlogging.UrLogging, urhtml.UrHtml):
  def __init__(self, debug=False, verbose=False):
    urlogging.UrLogging.__init__(self, debug=debug, verbose=verbose)
    self.rules = []

  def tokenize(self, line):
    for token in shlex.split(line):
      yield token

  def load(self, rules):
    for line in rules.split('\n'):
      if line and len(line):
        print('LINE={}'.format(line))

        for token in self.tokenize(line):
          print('TOKEN={}'.format(token))
          if token[0] == '#':
            break

          rule = []
          for action in line.split(' '):
            print('ACTION={}'.format(action))
            if action.endswith('()'):
              if re.search(r'=', action):
                v, f = action.split('=')
                rule.append(('function-returns', v, f))
              else:
                rule.append(('function', action))
              continue
            if re.search(r'=', action):
              a, v = action.split('=')
              rule.append(('attribute=', a, v))
              continue
            rule.append(('tag', action))
          self.rules.append(rule)

  def print_rules(self):
    for i, rule in enumerate(self.rules):
      print(i, rule)

  def apply(self, filename):
    pass

if __name__ == '__main__':
  up = UrParse()
  up.fatal('{} is a library'.format(sys.argv[0]))
  sys.exit(0)
