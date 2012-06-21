#!/usr/bin/env python

import urllib2
from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self, region='us-east-1', arch='64-bit', storage='ebs'):
        self.image = ''
        self.region = region
        self.arch = arch
        self.storage = storage

        self.reset()
        self.is_region = False
        self.is_arch = False
        self.is_storage = False

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.is_region = False
            self.is_arch = False
            self.is_storage = False

    def handle_data(self, data):
        text = data.strip()
        if self.is_region and self.is_arch and self.is_storage and text.startswith('ami-'):
            print text
        elif text == self.region:
            self.is_region = True
        elif self.is_region and text == self.arch:
            self.is_arch = True
        elif self.is_arch and text == self.storage:
            self.is_storage = True

    def get_image_name(self):
        return self.image

page = urllib2.urlopen('http://cloud-images.ubuntu.com/precise/current/')
text = page.read()

parser = MyHTMLParser()
parser.feed(text)
