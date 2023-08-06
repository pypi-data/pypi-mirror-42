# vim: fdm=indent
# author:     Fabio Zanini
# date:       14/08/17
# content:    Feature sheet with metadata.
# Modules
import pandas as pd


# Classes / functions
class FeatureSheet(pd.DataFrame):
    _metadata = ['sheetname']

    @property
    def _constructor(self):
        return FeatureSheet

    @classmethod
    def from_sheetname(cls, sheetname):
        from .io import parse_featuresheet

        self = cls(parse_featuresheet({'sheetname': sheetname}))
        self.sheetname = sheetname

        return self

    @classmethod
    def from_datasetname(cls, datasetname):
        from .io import parse_featuresheet

        self = cls(parse_featuresheet({'datasetname': datasetname}))
        self.sheetname = datasetname

        return self
