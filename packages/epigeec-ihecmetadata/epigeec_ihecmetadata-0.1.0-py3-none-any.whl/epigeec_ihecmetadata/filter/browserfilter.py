# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy
import collections

BROWSER = 'browser'
SUPPORTED_SIGNAL_TYPES = ["methylation_profile", "signal_forward", "signal_unstranded", "signal", "signal_reverse"]

def filter_supported_browser_type(ihec_metadata):
    """This filter browser with supported type from the source `IhecMetadata`.

        args:
            ihec_metadata: A `IhecMetadata` source.
        returns:
            A `IhecMetadata` with supported signal types only."""
    ihec_metadata_copy = copy.deepcopy(ihec_metadata)

    for dn in ihec_metadata_copy.datasets.keys():
        for bn in ihec_metadata_copy.datasets[dn].get(BROWSER, {}).keys():
            if bn not in SUPPORTED_SIGNAL_TYPES:
                del ihec_metadata_copy.datasets[dn][BROWSER][bn]

    return ihec_metadata_copy

def filter_out_empty_browser_dataset(ihec_metadata):
    """This filter out dataset with empty browser from the source `IhecMetadata`.

        args:
            ihec_metadata: A `IhecMetadata` source.
        returns:
            A `IhecMetadata` with no empty browser."""
    ihec_metadata_copy = copy.deepcopy(ihec_metadata)

    for dn in ihec_metadata_copy.datasets.keys():
        if ihec_metadata_copy.datasets[dn].get(BROWSER, {}):
            del ihec_metadata_copy.datasets[dn]

    return ihec_metadata_copy