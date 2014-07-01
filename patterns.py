#!/usr/bin/env python
import urllib2
import urllib
from bs4 import BeautifulSoup


class SubtlePatterns:
    url = 'http://subtlepatterns.com'

    def __init__(self):
        self.urls = []
        self.get_image_urls()

    def get_image_urls(self):
        opener = urllib2.build_opener()
        
        # Set range 39 to how many pagination pages subtlepatters.com got. It's currently 39
        for counter in range(39, 0, -1):
            self.urls.append('%s/page/%s' % (self.url, counter))

        try:
            for url in self.urls:
                html = BeautifulSoup(opener.open(url).read())
                hrefs = html.findAll('a', { 'class': 'download'})

                for href in hrefs:
                    self.download_zips('%s%s' % (self.url, href['href']))
                                    
        except Exception, e:
            print e

    def download_zips(self, zipurl):
        zipname = zipurl.split('/')[-1]
        print 'downloading %s ..' % zipname

        urllib.urlretrieve(zipurl, 'zips/%s' % zipname)

if __name__ == '__main__':
    SubtlePatterns()
