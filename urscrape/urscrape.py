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

import sys
import os
import io
import re
from urscrape import urlogging
from urscrape import urhtml
from urllib import request
from urllib.error import URLError
from urllib.parse import urlparse
import subprocess
import time
from collections import deque
import lxml.html
import random

class UrScrape(urlogging.UrLogging,urhtml.UrHtml):
    def __init__(self, debug=False, verbose=False):
        urlogging.UrLogging.__init__(self, debug=debug, verbose=verbose)

        self.urls = deque()
        self.urls_seen = set()
        self.prev_url = None

        self.considered_count = 0
        self.cached_count = 0
        self.fetched_count = 0
        self.queued_count = 0

        # defaults
        self.delay = (9, 11) # seconds of delay
        self.kinds = None

    def restrict(self, kinds):
        self.kinds = kinds

    def pathquery2cachefile(self, path, query):
        basename = os.path.basename(path)
        if not query:
            return basename
        return basename + '_' + query

    def url2cachefile(self, url):
        _, _, path, params, query, fragment = urlparse(url)
        return self.pathquery2cachefile(path, query)

    def url_to_descriptor(self, url):
        '''Given a url, return a tuple of the following form:
        (kind, parser, refetch_seconds, delay_seconds)

        If kind is None, the url will be ignored.

        If parser is not None, then it should be a function that parses
        the page.

        '''
        return (None, None, self.refetch_seconds, self.delay_seconds)

    def clean_url(self, url):
        return url

    def parse(self, tree):
        return None

    def add_url(self, url, kind, parser=self.href_scan, parser_args=self,
                refetch_seconds=self.refetch_seconds,
                delay_range=self.delay_range):
        if kind == None:
            return
        if url = self.prev_url:
            return
        self.prev_url = url
        if url in self.urls_seen:
            self.info('Seen {}: {}'.format(kind, url))
            return
        self.info('{}: {}'.format(kind, url))
        self.queued_count += 1
        self.urls_seen.add(url)
        self.urls.append((url, kind, parser, parser_args,
                          refetch_seconds, delay_range))

    def _sleep(self, delay_range, longer=False):
        delay = random.randrange(delay_range[0], delay_range[1])
        if longer:
            delay *= 2
        self.info('Sleeping {}s'.format(delay))
        time.sleep(delay)

    def _scrape(self):
        while True:
            try:
                (url, kind, parser, parser_args,
                 refetch_seconds, delay_range) = self.urls.popleft()
            except IndexError:
                url = None
            if url == None:
                break

            file = self._fetch(url, refetch_seconds)
            if not file:
                if self.local_only or self.index_only or self.data_only:
                    continue
                self.info('Unexpected failure')
                self._sleep(delay_range, longer=True)
                continue

            if parser:
                parser(parser_args, file)

    def href_scan(self, file):
        tree = self._get_tree(file)
        urls = self._find_urls(tree)
        for url in urls:
            self._add_url(url)

        if url_type == self.DATA:
            self.parse(tree)


    def _get_tree(self, file):
        with open(file, 'rb') as fp:
            tree = lxml.html.fromstring(fp.read().decode('utf-8'))
        return tree

    def _find_urls(self, tree):
        return tree.xpath('//a/@href')

    def _fetch(self, url, url_type):
        if self.index_only and url_type != self.INDEX:
            return None
        if self.data_only and url_type != self.DATA:
            return None

        if url_type == self.INDEX:
            refetch_seconds = self.index_time
        elif url_type == self.DATA:
            refetch_seconds = self.data_time
        else:
            refetch_seconds = 3600

        self.considered_count += 1
        self.info('Considering {}'.format(url))
        self.info('queued={} considered={} cached={} fetched={}'.format(
            self.queued_count, self.considered_count, self.cached_count,
            self.fetched_count))
        file = self.url2cachefile(url)
        try:
            dir = self.cachedir
        except:
            dir = '.cache'
        file = os.path.join(dir, file)
        dirname = os.path.dirname(file)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        if os.path.exists(file):
            mtime = os.path.getmtime(file)
            age = time.time() - mtime
            print('age={}'.format(age))
            if age < refetch_seconds or self.local_only:
                hours = int(age // 3600)
                minutes = int((age - hours * 3600) // 60)
                seconds = int(age - hours * 3600 - minutes * 60)
                self.info('Using cached {0} (age={1:02d}:{2:02d}:{3:02d})'
                          .format(file, hours, minutes, seconds))
                self.cached_count += 1
                return file

        if self.local_only:
            self.info('Not scraping {}'.format(url))
            return None

        self.info('Scraping {0} to {1}'.format(url, file))

        req = request.Request(url,
                              headers={'Accept-encoding': 'gzip'})

        try:
            res = request.urlopen(req, timeout=10)
        except:
            self.error_decode('Cannot open {}'.format(url))
            return None

        if url != res.geturl():
            self.error('URL redirected to: {}'.format(res.geturl()))

        if res.info().get('Content-Encoding') == 'gzip':
            p = subprocess.Popen(['zcat', '-q'],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
            data, serr = p.communicate(input=res.read())
            p.wait()
        else:
            data = res.read()
        with open(file, 'wb') as fp:
            fp.write(data)
        self.fetched_count += 1
        self._sleep()
        return file

if __name__ == '__main__':
    us = UrScrape()
    us.fatal('%s is a library', sys.argv[0])
