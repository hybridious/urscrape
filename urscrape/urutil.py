#!/usr/bin/python3
# -*-python-*-
'''
Copyright 2014 Pham Urwen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import sys
import argparse

class LicenseAction(argparse.Action):
    def __call__(self, parser, *args, **kwargs):
        print('{0}'.format(get_standard_license()))
        parser.exit()

class ErrorHandler(argparse.ArgumentParser):
    def error(self, message):
        print('\nerror: {0}\n'.format(message))
        self.print_help()
        sys.exit(1)

def get_parser(description=None):
    return ErrorHandler(description=description)

def add_standard_arguments(parser, version):
    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(version))
    parser.add_argument('--verbose', action='store_true',
                        help='log verbose informational messages')
    parser.add_argument('--debug', action='store_true',
                        help='log debugging messages')
    parser.add_argument('--license', action=LicenseAction, nargs=0,
                        help='display license')
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.description += '''

This program is OPEN SOURCE software.  Use --license to display license.
'''

def get_standard_license():
    return \
'''
Copyright 2014 Pham Urwen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

if __name__ == '__main__':
    ul = UrLogging()
    ul.fatal('%s is a library', sys.argv[0])
