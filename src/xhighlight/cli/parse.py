import argparse
import re
import sys


argparser = argparse.ArgumentParser(
    description="Highlight regions on the screen."
)

argparser.add_argument(
    'region_specs',
    nargs='*',
    type=str,
    metavar='[r|e]w×h+x+y',
    help=(
        "A region specification 'e' for ellipsoid highlights, 'r' for "
        "rectangular highlights. If the type is not supplied, assume 'r'."
    )
)

argparser.add_argument(
    '--opacity', '-o',
    type=float,
    default=.8,
    help="Opacity of the dim overlay (0 ≤ o ≤ 1), where 1 is perfectly opaque."
)


region_spec_re = re.compile(r"""
    ^
    (?P<type>r|R|e|E)?
    (?P<width>\d+)
    [×xX]
    (?P<height>\d+)
    \+
    (?P<x>\d+)
    \+
    (?P<y>\d+)
    $
""", re.X)


def parse_region_spec(region_spec):

    parsed = region_spec_re.match(region_spec)

    try:
        spec = parsed.groupdict()
        if not spec['type']:
            spec['type'] = 'r'
        else:
            spec['type'] = spec['type'].lower()
        return {
            k: int(v) if not k == 'type' else v
            for (k, v) in spec.items()
        }

    except (AttributeError, ValueError):
        raise ValueError("Malformed region spec: %s" % region_spec)


def parse_region_specs(args):

    regions = []
    for region_spec in args.region_specs:

        try:
            region = parse_region_spec(region_spec)

        except ValueError as exc:
            print(exc, file=sys.stderr)
            sys.exit(1)

        else:
            regions.append(region)

    return regions
