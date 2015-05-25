#!/usr/bin/python3
# -*-python-*-
'''
Copyright 2014,2015 Pham Urwen

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

import io
import lxml.html
import os
import random
import re
import socket
import subprocess
import sys
import time

from collections import deque
from urllib import request
from urllib.error import URLError
from urllib.parse import urlparse
from urscrape import urhtml
from urscrape import urlogging

class UrScrape(urlogging.UrLogging, urhtml.UrHtml):
    def __init__(self, debug=False, verbose=False):
        urlogging.UrLogging.__init__(self, debug=debug, verbose=verbose)

        self.urls = deque()
        self.urls_seen = set()
        self.prev_url = None

        self.considered_count = 0
        self.cached_count = 0
        self.fetched_count = 0
        self.queued_count = 0

        # defaults that can be set using self.config()
        self.local_only = False
        self.kinds = None
        self.delay_range = (8, 12) # seconds of delay
        self.base_url = None
        self.cachedir = '.cache'

        # defaults that can be set
        self.compression = True
        self.timeout = 10
        self.headers = None
        self.byte_limit = 0
        self.agent = 'SemanticBot 0.7beta'

    def config(self, local_only=None, kinds=None, delay_range=None):
        if local_only != None:
            self.local_only = local_only
        if kinds != None:
            self.kinds = kinds
        if delay_range != None:
            self.delay_range = delay_range

    def pathquery2cachefile(self, path, query, kind):
        basename = os.path.basename(path)
        if not query:
            return basename
        return kind + '-' + basename + '-' + query

    def url2cachefile(self, url, kind):
        _, _, path, params, query, fragment = urlparse(url)
        return self.pathquery2cachefile(path, query, kind)

    def url_to_descriptor(self, url):
        '''Given a url, return a tuple of the following form:
        (url, kind, parser, parser_args, refetch_seconds)

        If kind is None, the url will be ignored.

        If parser is not None, then it should be a function that parses
        the page.

        '''
        return (None, None, None, None, self.refetch_seconds)

    def clean_url(self, url):
        return url

    def add_url(self, url, kind, parser=None, parser_args=None,
                refetch_seconds=None, delay_range=None):
        if not self.base_url:
            self.base_url = url
        if kind == None:
            return
        if url == self.prev_url:
            return
        self.prev_url = url
        if url in self.urls_seen:
            self.info('Seen {}: {}'.format(kind, url))
            return
        if refetch_seconds == None:
            refetch_seconds = self.refetch_seconds
        if delay_range == None:
            delay_range = self.delay_range
        self.info('{}: {}'.format(kind, url))
        self.queued_count += 1
        self.urls_seen.add(url)
        self.urls.append((url, kind, parser, parser_args,
                          refetch_seconds, delay_range))
        if not self.queued_count % 100:
            self.info('Shuffling list of urls')
            random.shuffle(self.urls)

    def _sleep(self, delay_range, longer=False):
        try:
            delay = random.randrange(delay_range[0], delay_range[1])
        except:
            delay = delay_range[0]
        if longer:
            delay *= 2
        self.info('Sleeping {}s'.format(delay))
        time.sleep(delay)

    def _scrape(self):
        failures = 0
        while True:
            try:
                (url, kind, parser, parser_args,
                 refetch_seconds, delay_range) = self.urls.popleft()
            except IndexError:
                url = None
            if url == None:
                break

            file = self._fetch(url, kind, refetch_seconds, delay_range)
            if file == 0:
                # Skip
                continue
            if not file:
                failures += 1
                if failures >= 10:
                    self.error('{} failures, terminating scrape'.format(
                        failures))
                    return
                continue

            if parser:
                parser(file)

    def _get_tree(self, file):
        with open(file, 'rb') as fp:
            try:
                tree = lxml.html.fromstring(fp.read()
                                            .decode('utf-8')
                                            .replace(u'\xa0', u' '))
            except:
                self.info('Using latin-1 instead of utf-8 for {}'.format(file))
                fp.seek(0)
                tree = lxml.html.fromstring(fp.read()
                                            .decode('latin-1'))
        return tree

    def _find_urls(self, tree):
        return tree.xpath('//a/@href')

    def href_scan(self, file):
        tree = self._get_tree(file)
        tree.make_links_absolute(self.base_url)
        urls = self._find_urls(tree)
        for url in urls:
            url = self.clean_url(url)
            descriptors = self.url_to_descriptor(url)
            if isinstance(descriptors, tuple):
                self.add_url(*descriptors)
            else:
                for descriptor in descriptors:
                    self.add_url(*descriptor)

    def _fetch(self, url, kind, refetch_seconds, delay_range):
        use_local = False
        if self.local_only or (self.kinds and kind not in self.kinds):
            use_local = True

        self.considered_count += 1
        self.info('Considering {} {}'.format(kind, url))
        self.info('queued={} considered={} cached={} fetched={}'.format(
            self.queued_count, self.considered_count, self.cached_count,
            self.fetched_count))
        file = self.url2cachefile(url, kind)
        file = os.path.join(self.cachedir, file)

        # Find dirname, since url2cachefile might have a subdirectory
        # structure.
        dirname = os.path.dirname(file)

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        if os.path.exists(file):
            mtime = os.path.getmtime(file)
            age = time.time() - mtime
            hours = int(age // 3600)
            minutes = int((age - hours * 3600) // 60)
            seconds = int(age - hours * 3600 - minutes * 60)
            if age < refetch_seconds or use_local:
                self.info('Using cached {0} (age={1:02d}:{2:02d}:{3:02d})'
                          .format(file, hours, minutes, seconds))
                self.cached_count += 1
                return file
            else:
                self.info('Refetching cached {} {} (age={:02d}:{:02d}:{:02d})'
                          .format(kind, file, hours, minutes, seconds))

        if use_local:
            self.info('Skipping {0} to {1}'.format(url, file))
            return 0 # Special marker for skips

        self.info('Scraping {0} to {1}'.format(url, file))

        tries = 0
        fetched = False
        while tries < 3:
            tries += 1
            if tries > 1:
                self.error('Re-scraping {} to {}, try {}'.format(url,
                                                                 file,
                                                                 tries))
            req = request.Request(url)
            if self.compression:
                req.add_header('Accept-encoding', 'gzip')
            if self.agent:
                req.add_header('User-agent', self.agent)
            if self.headers:
                for k, v in self.headers:
                    req.add_header(k, v)

            try:
                res = request.urlopen(req, timeout=self.timeout)
            except:
                self.error_decode('Cannot open {}'.format(url))
                self.error('Delaying...')
                self._sleep(delay_range, longer=True)
                break

            if url != res.geturl():
                self.error('URL redirected to {}'.format(res.geturl()))

            try:
                if self.byte_limit:
                    data = res.read(self.byte_limit)
                else:
                    data = res.read()
            except socket.timeout:
                self.error('Timeout on {}'.format(url))
                continue

            fetched = True
            break

        if not fetched:
            self.error('Could not fetch {}'.format(url))
            return None

        # Decompress if necessary.
        if res.info().get('Content-Encoding') == 'gzip':
            p = subprocess.Popen(['zcat', '-q'],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
            data, serr = p.communicate(input=data)
            p.wait()

        with open(file, 'wb') as fp:
            fp.write(data)
        self.fetched_count += 1
        self._sleep(delay_range)
        return file

if __name__ == '__main__':
    us = UrScrape()
    us.fatal('%s is a library', sys.argv[0])
