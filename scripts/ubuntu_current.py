#!/usr/bin/env python

import urllib2
from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.reset()
        self.inside_tr = False
        self.inside_td = False
        self.inside_p = False
        self.inside_a = False
        self.inside_tt = False

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.inside_tr = True
        elif self.inside_tr and tag == 'td':
            self.inside_td = True
        elif self.inside_td and tag == 'p':
            self.inside_p = True
        elif self.inside_p and tag == 'a':
            self.inside_a = True
        elif self.inside_a and tag == 'tt':
            self.inside_tt = True

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.inside_tr = False
            self.inside_td = False
            self.inside_p = False
            self.inside_a = False
            self.inside_tt = False

    def handle_data(self, data):
        if self.inside_tt and data.startswith('ami'):
            print data

        if data.strip():
            if self.inside_p and not self.inside_a and not self.inside_tt and data.strip() not in ['us-east-1', '64-bit', 'ebs']:
                self.inside_tr = False
                self.inside_td = False
                self.inside_p = False
                self.inside_a = False
                self.inside_tt = False

page = urllib2.urlopen('http://cloud-images.ubuntu.com/precise/current/')
text = page.read()

parser = MyHTMLParser()
parser.feed(text)
