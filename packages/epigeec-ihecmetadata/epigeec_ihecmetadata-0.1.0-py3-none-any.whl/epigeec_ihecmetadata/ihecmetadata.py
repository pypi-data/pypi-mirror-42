# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

class IhecMetadata(object):
    """It's a representation of a JSON from the IHEC DataPortal."""
    def __init__(self, datasets, samples, hub_description):
        """
            args:
                datasets: Mapping of datasets
                samples: Mapping of samples
                hub_description: Mapping of hub_description"""
        self._datasets = datasets
        self._samples = samples
        self._hub_description = hub_description

    @property
    def datasets(self):
        """Return Mapping of datasets"""
        return self._datasets

    @property
    def samples(self):
        """Return Mapping of samples"""
        return self._samples

    @property
    def hub_description(self):
        """Return Mapping of hub_description"""
        return self._hub_description
