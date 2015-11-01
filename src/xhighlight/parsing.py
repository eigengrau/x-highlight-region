import argparse
from xhighlight.region import Region, Shape


class RegionAction (argparse.Action):

    def __init__(self, *args, shape=None, **kwargs):

        if shape is None:
            raise ValueError("region_type must be set.")

        super().__init__(*args, **kwargs)
        self.default = []
        self.shape = shape
        self.metavar = ('X', 'Y', 'WIDTH', 'HEIGHT')

    def __call__(self, parser, namespace, values, option_string):

        regions = getattr(namespace, self.dest)
        if regions is None:
            regions = []
            setattr(namespace, self.dest, regions)
        region = Region(self.shape, *values)
        regions.append(region)
