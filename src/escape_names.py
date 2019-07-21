#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class Escape:
    def __init__(self):
        self.filenames = []

    def list_files(self, dir):
        g = os.walk(dir)
        for root, dirs, files in g:
            for filename in files:
                if filename.endswith('.html'):
                    filename = self.escape(filename)
                    print(filename)
                    self.filenames.append(filename)

    def escape(self, s):
        return s.replace('-', ':').replace('_', '/')[:-5]


dir = r'C:\Users\Kohaku\Source\Repos\scrapy_dir\tutorial'
escape = Escape()
escape.list_files(dir)
