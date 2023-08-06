import argparse

from . import builder

parser = argparse.ArgumentParser(
    description='Garden of Eden Creation Kit',
    usage='geck builder SCRIPT run',
)

subparsers = parser.add_subparsers()
builder_parser = subparsers.add_parser(
    'builder', 
    help='Use the geck builder',
    usage='geck builder SCRIPT run',
)
builder_parser.set_defaults(func=builder.build)
builder_parser.add_argument(
    'script',
    help='The GECK build script',
)
builder_parser.add_argument(
    'action',
    choices=['run'],
    help='The action to take',
)
