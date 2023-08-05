from copy import deepcopy
import os
import sys
import logging
import argparse

import satsearch.config as config

from satstac.utils import dict_merge
from .version import __version__


class SatUtilsParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        """ Initialize a SatUtilsParser """
        super(SatUtilsParser, self).__init__(*args, **kwargs)
        self.formatter_class = argparse.ArgumentDefaultsHelpFormatter

        self.pparser = argparse.ArgumentParser(add_help=False)
        self.pparser.add_argument('--version', help='Print version and exit', action='version', version=__version__)
        self.pparser.add_argument('-v', '--verbosity', default=2, type=int,
                            help='0:quiet, 1:error, 2:warning, 3:info, 4:debug')

        self.download_parser = argparse.ArgumentParser(add_help=False)
        self.download_group = self.download_parser.add_argument_group('download options')
        self.download_group.add_argument('--datadir', help='Directory pattern to save assets', default=config.DATADIR)
        self.download_group.add_argument('--filename', default=config.FILENAME,
                           help='Save assets with this filename pattern based on metadata keys')
        self.download_group.add_argument('--download', help='Download assets', default=None, nargs='*')
        h = 'Acknowledge paying egress costs for downloads (if in request pays bucket)'
        self.download_group.add_argument('--requestor-pays', help=h, default=False, action='store_true', dest='requestor_pays')

        self.output_parser = argparse.ArgumentParser(add_help=False)
        self.output_group = self.output_parser.add_argument_group('output options')
        h = 'Print specified metadata for matched scenes'
        self.output_group.add_argument('--print-md', help=h, default=None, nargs='*', dest='printmd')
        h = 'Print calendar showing dates'
        self.output_group.add_argument('--print-cal', help=h, default=False, action='store_true', dest='printcal')
        self.output_group.add_argument('--save', help='Save results as GeoJSON', default=None)

    def parse_args(self, *args, **kwargs):
        """ Parse arguments """
        args = super(SatUtilsParser, self).parse_args(*args, **kwargs)
        args = vars(args)
        args = {k: v for k, v in args.items() if v is not None}

        if args.get('command', None) is None:
            self.print_help()
            sys.exit(0)

        # set logging level
        if 'verbosity' in args:
            logging.basicConfig(stream=sys.stdout, level=(50-args.pop('verbosity') * 10))

        # set global configuration options
        if 'url' in args:
            config.API_URL = args.pop('url')
        if 'datadir' in args:
            config.DATADIR = args.pop('datadir')
        if 'filename' in args:
            config.FILENAME = args.pop('filename')

        return args

    @classmethod
    def newbie(cls, *args, **kwargs):
        """ Create a newbie class, with all the skills needed """
        parser = cls(*args, **kwargs)
        subparser = parser.add_subparsers(dest='command')
        parents = [parser.pparser, parser.output_parser]

        sparser = subparser.add_parser('search', help='Perform new search of items', parents=parents)
        """ Adds search arguments to a parser """
        parser.search_group = sparser.add_argument_group('search options')
        parser.search_group.add_argument('-c', '--collection', help='Name of collection', default=None)
        h = 'One or more scene IDs from provided collection (ignores other parameters)'
        parser.search_group.add_argument('--ids', help=h, nargs='*', default=None)
        parser.search_group.add_argument('--bbox', help='Bounding box (min lon, min lat, max lon, max lat)', nargs=4)
        parser.search_group.add_argument('--intersects', help='GeoJSON Feature (file or string)')
        parser.search_group.add_argument('--datetime', help='Single date/time or begin and end date/time (e.g., 2017-01-01/2017-02-15)')
        parser.search_group.add_argument('-p', '--property', nargs='*', help='Properties of form KEY=VALUE (<, >, <=, >=, = supported)')
        parser.search_group.add_argument('--sort', help='Sort by fields', nargs='*')
        h = 'Only output how many Items found'
        parser.search_group.add_argument('--found', help=h, action='store_true', default=False)
        parser.search_group.add_argument('--url', help='URL of the API', default=config.API_URL)

        parents.append(parser.download_parser)
        lparser = subparser.add_parser('load', help='Load items from previous search', parents=parents)
        lparser.add_argument('items', help='GeoJSON file of Items')
        return parser

    class KeyValuePair(argparse.Action):
        """ Custom action for getting arbitrary key values from argparse """
        def __call__(self, parser, namespace, values, option_string=None):
            for val in values:
                n, v = val.split('=')
                setattr(namespace, n, {'eq': v})
