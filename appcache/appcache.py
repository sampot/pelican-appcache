# -*- coding: utf-8 -*-
"""
Appcache
-------

The plugin generates manifest file for HTML5 application cache.
"""

from __future__ import unicode_literals, print_function

import os.path

from datetime import datetime
from logging import info
from codecs import open

from pelican import signals


MANIFEST_HEADER = """CACHE MANIFEST
# Last updated: {timestamp}
"""

MANIFEST_NETWORK = """
NETWORK:
*
"""

MANIFEST_FALLBACK = """
FALLBACK:
/thumbnails/small /thumbnails/small/featured_image.jpg
"""


def format_date(date):
    if date.tzinfo:
        tz = date.strftime('%z')
        tz = tz[:-2] + ':' + tz[-2:]
    else:
        tz = "-00:00"
    return date.strftime("%Y-%m-%dT%H:%M:%S") + tz

class AppCacheGenerator(object):

    def __init__(self, context, settings, path, theme, output_path, *null):

        self.output_path = output_path
        self.context = context
        self.now = datetime.now()
        self.siteurl = settings.get('SITEURL')
        self.articles_per_page = settings.get('DEFAULT_PAGINATION', 8)
        self.orphans = settings.get('DEFAULT_ORPHANS', 2)

        self.manifest_name = settings.get('APPCACHE_MANIGEST_NAME', 'manifest.appcache')
        self.resources = settings.get("APPCACHE_RESOURCES", [])

    def write_url(self, page, fd):

        if getattr(page, 'status', 'published') != 'published':
            return

        # We can disable categories/authors/etc by using False instead of ''
        if not page.save_as:
            return

        page_path = os.path.join(self.output_path, page.save_as)
        if not os.path.exists(page_path):
            return

        pageurl = '{siteurl}/{uri}'.format(siteurl=self.siteurl, uri=page.url)
        
        fd.write(pageurl)
        fd.write('\n')

    def sanitize_pages(self, pages):
        result = []
        for page in pages:
            if getattr(page, 'status', 'published') == 'published':
                result.append(page)
        return result

    def generate_output(self, writer):
        path = os.path.join(self.output_path, self.manifest_name)

        articles = self.sanitize_pages(self.context['articles'])
        article_count = len(articles)
        # print("Total articles: ", article_count)
        num_pages = article_count / self.articles_per_page
        pages = self.context['pages'] + articles

        for article in self.context['articles']:
            pages += article.translations

        info('writing {0}'.format(path))

        with open(path, 'w', encoding='utf-8') as fd:
            fd.write(MANIFEST_HEADER.format(timestamp=format_date(self.now)))

            # index page(s)
            fd.write(self.siteurl + '/index.html\n')
            num_pages -= 1  # decreases by 1 for /index.html page
            remaining = (article_count % self.articles_per_page)
            if 0 < remaining < self.orphans:
                num_pages -= 1
            # print("Total pages: ", num_pages)

            page_template = '/page/{num}/\n'
            for n in range(num_pages):
                fd.write(self.siteurl + page_template.format(num=n+2))

            for res in self.resources:
                fd.write(self.siteurl + '/' + res)
                fd.write('\n')

            for page in pages:
                self.write_url(page, fd)

            fd.write(MANIFEST_NETWORK)
            fd.write(MANIFEST_FALLBACK)

def get_generators(generators):
    return AppCacheGenerator


def register():
    signals.get_generators.connect(get_generators)
