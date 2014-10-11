<<<<<<< 615b6908ce30ab4bce00847071e2a1f35f403860
#!/usr/bin/env python3
# urscrape.py -*-python-*-
# Copyright 2016 by urwen (urwen@mail.ru)
# This program comes with ABSOLUTELY NO WARRANTY.

from urscrape.log import *

INFO("urscrape.py")

=======
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
import os
from urscrape import urlogging

class UrScrape(urlogging.UrLogging):
    def __init__(self, debug=False, verbose=False):
        urlogging.UrLogging.__init__(self, debug=debug, verbose=verbose)

    def scrape_(self):
        try:
            self.info('Scraping {0}'.format(self.site))
        except:
            self.fatal('self.site not set to the root of the site to scrape')
        self.fetch_(self.site)

    def url2cachefile(self, url):
        try:
            dir = self.cachedir
        except:
            dir = '.cache'

        if url.endswith('.html'):
            cachefile = os.path.join(dir, 

    def fetch_(self, url):
        file = self.url2cachefile(url)

if __name__ == '__main__':
    us = UrScrape()
    us.fatal('%s is a library', sys.argv[0])
>>>>>>> Checkpoint
