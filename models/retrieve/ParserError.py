#!usr/bin/env python3
import logging
logger = logging.getLogger(__name__)


class ParserError:

    def __init__ (self, type, description):
        self.type = type
        self.description = description

    def __str__ (self):
        return "[%s] %s" % (self.type, self.description)
