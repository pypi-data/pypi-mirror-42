# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import collections

from ..ihecmetadata import IhecMetadata

class IhecJsonEncode(json.JSONEncoder):
    def __init__(self, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None, separators=None, default=None):
        super(IhecJsonEncode, self).__init__(skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan, sort_keys=sort_keys, indent=indent, separators=separators, default=default)

    def default(self, ihec_metadata): # pylint: disable=E0202
        try:
            return [
                ('datasets', ihec_metadata.datasets),
                ('samples', ihec_metadata.samples),
                ('hub_description', ihec_metadata.hub_description)
            ]
        except:
            return super(IhecJsonEncode, self).default(ihec_metadata)

    def encode(self, ihec_metadata):
        super(IhecJsonEncode, self).encode(self.default(ihec_metadata))

    def iterencode(self, ihec_metadata):
        super(IhecJsonEncode, self).iterencode(self.default(ihec_metadata))