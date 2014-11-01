import os
import sys
import re
import html
from urscrape import urscrape

class Scraper(urscrape.UrScrape):
    def __init__(self, debug=False, verbose=False):
        urscrape.UrScrape.__init__(self, debug=debug, verbose=verbose)
        self.refetch_seconds = 3 * 24 * 3600
        self.long_refetch_seconds = 31 * 24 * 3600
        self.delay_second = [3, 7]
        self.add_url('https://www.commonsensemedia.org/tv-reviews',
                     self.parse_index, self)
        self.add_url('https://www.commonsensemedia.org/movie-reviews',
                     self.parse_index, self)

    def url_to_descriptor(self, url):
        basename = os.path.basename(url)
        if basename in [ 'dvd', 'theaters' ]:
            return (None, None, None, None)
        if 'user-reviews' in url:
            return (None, None, None, None)
        if 'page=' in url or \
           url.endswith('tv-reviews') or url.endswith('movie-reviews'):
            return ("index", self.parse_index, self)
        if 'movie-reviews/' in url or 'tv-reviews/' in url:
            return ("data", self.parse_index, self, self.long_refetch_seconds)
        return (None, None, None, None)

    def clean_url(self, url):
        if 'rate=' in url:
            url = re.sub(r'\?rate=.*', '', url)
        return url

    def pathquery2cachefile(self, path, query):
        basename = os.path.basename(path)
        if not query:
            if 'tv-reviews/' in path:
                return 'tv-' + basename
            elif 'movie-reviews/' in path:
                return 'movie-' + basename
            else:
                return basename
        elif 'page=' in query:
            page = re.sub(r'[^\d]*(\d+)', r'\1', query)
            return basename + '-' + page
        return basename + '_' + query


    def parse(self, tree):
        review = tree.xpath("//meta[@property='reviewBody']/@content")[0]
        review = review.replace(u'\xa0', u' ')
        print('{}'.format(review))
        print(html.unescape(review))
        print(self.strip_tags(review))
        sys.exit(1)
