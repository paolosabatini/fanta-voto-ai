#/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)
import urllib.request


def get_html (url):
    fp = urllib.request.urlopen(url)
    return fp.read().decode("utf8")
