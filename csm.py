import os
from urscrape import urscrape

class Scraper(urscrape.UrScrape):
    def __init__(self, debug=False, verbose=False):
        urscrape.UrScrape.__init__(self, debug=debug, verbose=verbose)
        self.site = 'http://commonsensemedia.org'
