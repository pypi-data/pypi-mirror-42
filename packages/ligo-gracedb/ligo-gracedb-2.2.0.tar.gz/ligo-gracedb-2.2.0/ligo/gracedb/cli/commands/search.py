import argparse
import textwrap
import sys

from .base import RegisteredCommandBase, RegisteredSubCommandBase
from .utils import parse_delimited_string
from ..parsers import object_id_parser, superevent_id_parser, graceid_parser


###############################################################################
# Base command
###############################################################################
registry = []
class SearchCommand(RegisteredCommandBase):
    name = "search"
    description = "Get a list of events or superevents based on a search query"
    subcommands = registry


###############################################################################
# Subcommands - registered to base command automatically
###############################################################################
class SearchChildBase(RegisteredSubCommandBase):
    _registry = registry


class SearchSupereventsCommand(SearchChildBase):
    name = "superevents"
    description = "Get a list of superevents based on a search query"
    default_columns = \
        "superevent_id,preferred_event,gw_events,labels,far,links.files"
    client_func = "superevents"

    def add_custom_arguments(self, parser):
        parser.add_argument("query", type=str,
            help="Search query (surround with quotes)")
        parser.add_argument("--columns", type=str,
            help=("Comma-separated list of parameters to show for each search "
            "result. Use '.' to get nested parameters (ex: 'links.files')"),
            default=self.default_columns)
        parser.add_argument("--max-results", type=int,
            help="Maximum number of results to show", default=None)
        return parser

    def run(self, client, args):
        # Get list of "columns" (or dict keys) from args
        column_list = parse_delimited_string(args.columns)

        # Call client function to get iterator
        func = getattr(client, self.client_func)
        events = func(args.query, max_results=args.max_results)

        output = []
        output.append(column_list)
        for ev in events:
            output.append([self.process_element(ev, col) for col in
                column_list])
        out = '#' + "\n".join(["\t".join(row) for row in output])
        return out

    def process_element(self, event, col):
        """
        Get values from nested dictionaries and join lists into
        comma-separated strings.
        """
        col_levels = col.split('.')
        a = event
        for c in col_levels:
            try:
                a = a[c]
            except KeyError as e:
                msg = ("'{col}' is not available in the response JSON. Check "
                    "the format on the server or by using '{prog} get' to "
                    "retrieve and individual event or superevent.").format(
                    col=col, prog=self.base_prog)
                print(msg)
                sys.exit(1)

        if isinstance(a, list):
            a = ",".join(a)
        return str(a)


class SearchEventsCommand(SearchSupereventsCommand):
    name = "events"
    description = "Get a list of events based on a search query"
    default_columns = \
        "graceid,labels,group,pipeline,far,gpstime,created"
    client_func = "events"
