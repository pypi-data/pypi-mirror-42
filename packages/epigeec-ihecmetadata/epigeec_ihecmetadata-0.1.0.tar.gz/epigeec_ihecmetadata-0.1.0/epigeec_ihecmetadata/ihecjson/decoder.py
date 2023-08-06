# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import collections

from ..ihecmetadata import IhecMetadata

class IhecJsonDecoder(json.JSONDecoder):
    def __init__(self, object_hook=collections.OrderedDict, parse_float=None, parse_int=None, parse_constant=None, strict=True):
        super(IhecJsonDecoder, self).__init__(object_hook=object_hook, parse_float=parse_float, parse_int=parse_int, parse_constant=parse_constant, strict=strict)

    def decode(self, s):
        return super(IhecJsonDecoder, self).decode(s)

    def raw_decode(self, s, idx=0):
        j, i = super(IhecJsonDecoder, self).raw_decode(s, idx=idx)
        return IhecMetadata(j['datasets'], j['samples'], j['hub_description']), i
