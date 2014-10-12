#!/usr/bin/env python
import urllib2
import urllib
import zipfile
import glob
import os
import fnmatch
import shutil
from bs4 import BeautifulSoup


class SubtlePatterns:
    url = 'http://subtlepatterns.com'
    urls = []

    def __init__(self):        
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.run()

    def run(self):
        self.folders()

        self.get_image_urls()
        
        self.parse_image_urls()
        
        self.sort_patterns()

        print 'Finished'

    def folders(self):
        paths = [
            '%s/zips/' % self.script_dir, 
            '%s/temp/' % self.script_dir, 
            '%s/patterns/' % self.script_dir
        ]

        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path, 0755)

    def get_patterns_site_id(self):
        opener = urllib2.build_opener()
        
        html = BeautifulSoup(opener.open(self.url).read())
        
        a = html.find('a', { 'class': 'last' })

        last_id = ''.join(id for id in a['href'] if id.isdigit())
        
        return int(last_id)

    def get_image_urls(self):
        last_id = self.get_patterns_site_id()

        for counter in range(last_id, 0, -1):
            self.urls.append('%s/page/%s' % (self.url, counter))
    
    def parse_image_urls(self):
        opener = urllib2.build_opener()        
        
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

    def sort_patterns(self):
        images = []        
        zips = self.get_zips()
        
        print 'Unpacking..'

        for zip in zips:
            self.unzip(source_filename=zip, dest_dir='%s/temp/' % self.script_dir)

        for root, dirnames, filenames in os.walk('%s/temp/' % self.script_dir):
            for filename in fnmatch.filter(filenames, '*.png'):
                images.append(os.path.join(root, filename))

        print 'Sort patterns..'

        for image in images:
            shutil.move(image, '%s/patterns/' % self.script_dir)

        print 'Deletes temp folder..'

        shutil.rmtree('%s/temp/' % self.script_dir)

    def get_zips(self):
        return glob.glob('%s/zips/*.zip' % self.script_dir)

    def unzip(self, source_filename, dest_dir):
        with zipfile.ZipFile(source_filename) as zf:
            zf.extractall(dest_dir)

if __name__ == '__main__':
    SubtlePatterns()
