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
import logging
import traceback

class UrLogging():
    def __init__(self, debug=False, verbose=False):
        logging.addLevelName(50, 'FATAL')
        logging.basicConfig(format='{levelname:1.1} {asctime} {message}',
                            style='{',
                            datefmt='%Y%m%d %H%M%S')
        self.logger = logging.getLogger('ur')
        self.loglevel(verbose, debug)

    def loglevel(self, verbose, debug):
        if verbose:
            self.logger.setLevel(logging.INFO)
        elif debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.WARNING)

    def fatal(self, message, *args, **kwargs):
        self.logger.critical(message, *args, **kwargs)
        self.logger.critical('Fatal termination...')
        sys.exit(-1)

    def error(self, message, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)

if __name__ == '__main__':
    ul = UrLogging()
    ul.fatal('%s is a library', sys.argv[0])
