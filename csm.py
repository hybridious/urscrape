import os
import sys
import re
import html
import html2text
from urscrape import urscrape

class Scraper(urscrape.UrScrape):
    def __init__(self, debug=False, verbose=False):
        urscrape.UrScrape.__init__(self, debug=debug, verbose=verbose)
        self.cachedir = '/db/csm'
        self.refetch_seconds = 7 * 24 * 3600
        self.long_refetch_seconds = 31 * 24 * 3600
        self.refetch_percent = 0
        self.refetch_index_percent = 100
        self.delay_second = [3, 7]
        self.add_url('https://www.commonsensemedia.org/tv-reviews',
                     'index', self.href_scan, self)
        self.add_url('https://www.commonsensemedia.org/movie-reviews',
                     'index', self.href_scan, self)

    def url_to_descriptor(self, url):
        basename = os.path.basename(url)
        if basename in [ 'dvd', 'theaters' ]:
            return (None, None, None, None, None)
        if 'user-reviews' in url:
            return (None, None, None, None, None)
        if 'page=' in url or \
           url.endswith('tv-reviews') or url.endswith('movie-reviews'):
            return (url, 'index', self.href_scan, self)
        if 'movie-reviews/' in url or 'tv-reviews/' in url:
            return (url, 'data', self.parse, None, self.long_refetch_seconds)
        return (None, None, None, None, None)

    def clean_url(self, url):
        if 'rate=' in url:
            url = re.sub(r'\?rate=.*', '', url)
        return url

    def pathquery2cachefile(self, path, query, kind):
        basename = os.path.basename(path)
        if not query:
            if 'tv-reviews/' in path:
                return kind + '-tv-' + basename
            elif 'movie-reviews/' in path:
                return kind + '-movie-' + basename
            else:
                return kind + '-' + basename
        elif 'page=' in query:
            page = re.sub(r'[^\d]*(\d+)', r'\1', query)
            return kind + '-' + basename + '-' + page
        return kind + '-' + basename + '-' + query
<<<<<<< 06ac4501aa9fb48842ce862f34614e73a635e67c
=======

    def add_xpath(self, tree, old_list, tag, xpath, func=None):
        result = tree.xpath(xpath)
        if not result:
            return old_list

        items = []
        for item in result:
            items.append(html2text.html2text(item))

        return old_list.append((tag, items))

    def dump_tags(self, tags, format=None):
        print('<entry>')
        for key, values in tags:
            print('  <{}>'.format(key))
            for value in values:
                print('    <item>{}</item>'.format(value))
            print('  </{}>'.format(key))
        print('</entry>')

    def parse(self, file):
        tags = []
        tree = self._get_tree(file)

        self.add_xpath(
            tree, tags, 'url',
            "//meta[@property='og:url']/@content")

        self.add_xpath(
            tree, tags, 'title',
            "//*[@property='itemReviewed']/meta[@property='name']/@content")

        self.add_xpath(
            tree, tags, 'rating',
            "//div[@property='reviewRating']/meta[@property='ratingValue']/@content")

        self.add_xpath(
            tree, tags, 'review',
            "//meta[@property='reviewBody']/@content")

        self.add_xpath(
            tree, tags, 'description',
            "//meta[@property='description']/@content")

        self.dump_tags(tags)

        actors = tree.xpath("//a[@property='actor']/text()")
        print('Actors: {}'.format(actors))

        company = tree.xpath(
            "//*[@property='productionCompany']/meta[@property='name']/@content")
        print('Company {}'.format(company))

        genres = []
        for e in tree.cssselect("td:contains('Genre:') + *"):
            for e2 in e:
                if e2.text:
                    genres.append(e2.text)
        print('Genres: {}'.format(genres))
>>>>>>> Checkpoint

    def add_xpath(self, tree, old_list, tag, xpath, func=None):
        result = tree.xpath(xpath)
        if not result:
            return old_list

        items = []
        for item in result:
            items.append(html2text.html2text(item))

        return old_list.append((tag, items))

    def dump_tags(self, tags, format=None):
        print('<entry>')
        for key, values in tags:
            print('  <{}>'.format(key))
            for value in values:
                print('    <item>{}</item>'.format(value))
            print('  </{}>'.format(key))
        print('</entry>')

    def print_text(self, ancestors, node):
        if isinstance(node.text, str) and node.tag not in ['style',
                                                           'script']:
            recent = ancestors[-1]
            if isinstance(node.tail, str):
                print('{}: {} {}'.format(recent, node.text.strip(),
                                         node.tail.strip()))
            else:
                print('{}: {}'.format(recent, node.text.strip()))
        elif node.tag == 'meta':
            recent = ancestors[-1]
            print('{}'.format(recent))

        for el in list(node):
            if isinstance(el.tag, str):
                desc = el.tag
                for key, value in el.attrib.iteritems():
                    desc += '[{}={}]'.format(key, value)
                self.print_text(ancestors + [ desc ], el)

#            print(el.tag)
#            if isinstance(el.tag, str) and isinstance(el.text, str):
##                text = el.text.strip()
#                if text != '' and el.tag not in ['style', 'script']:
#                    print('tag={} text={}'.format(el.tag, text))


    def parse(self, file):
        return # remove to work on parser
        tags = []
        tree = self._get_tree(file)

        self.print_text([], tree)

        self.add_xpath(
            tree, tags, 'url',
            "//meta[@property='og:url']/@content")

        self.add_xpath(
            tree, tags, 'title',
            "//*[@property='itemReviewed']/meta[@property='name']/@content")

        self.add_xpath(
            tree, tags, 'rating',
            "//div[@property='reviewRating']/meta[@property='ratingValue']/@content")

        self.add_xpath(
            tree, tags, 'review',
            "//meta[@property='reviewBody']/@content")

        self.add_xpath(
            tree, tags, 'description',
            "//meta[@property='description']/@content")

        self.dump_tags(tags)

        actors = tree.xpath("//a[@property='actor']/text()")
        print('Actors: {}'.format(actors))

        company = tree.xpath(
            "//*[@property='productionCompany']/meta[@property='name']/@content")
        print('Company {}'.format(company))

        genres = []
        for e in tree.cssselect("td:contains('Genre:') + *"):
            for e2 in e:
                if e2.text:
                    genres.append(e2.text)
        print('Genres: {}'.format(genres))

        sys.exit(1)
