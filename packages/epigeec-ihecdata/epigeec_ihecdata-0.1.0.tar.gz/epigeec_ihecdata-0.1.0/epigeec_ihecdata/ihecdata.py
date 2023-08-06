# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

class IhecData(object):
    def __init__(self, uri, basename, assembly, release):
        self.uri = uri
        self.basename = basename
        self.assembly = assembly
        self.release = release

    @property
    def found(self):
        return bool(self.uri)

    def __bool__(self):
        return self.found