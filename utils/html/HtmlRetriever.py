#/usr/bin/env python3
import logging
logger = logging.getLogger(__name__)
import urllib.request


def get_html (url):
    try:
        fp = urllib.request.urlopen(url)
        return fp.read().decode("utf8")
    except:
        logging.error ("[ERROR] Connection refused at %s" % url)
        exit(1)
