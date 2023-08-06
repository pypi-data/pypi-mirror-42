import argparse
import os
import textwrap

from .base import RegisteredCommandBase, RegisteredSubCommandBase
from .utils import parse_delimited_string, parse_delimited_string_or_single
from ..parsers import (
    object_id_parser, label_parser, comment_parser, tag_parser,
    superevent_id_parser,
)


###############################################################################
# Base command
###############################################################################
registry = []
class CreateCommand(RegisteredCommandBase):
    name = "create"
    description = textwrap.dedent("""\
        Create an event, superevent, log entry, signoff, EMObservation,
        or VOEvent
    """).rstrip()
    subcommands = registry


###############################################################################
# Subcommands - registered to base command automatically
###############################################################################
class CreateChildBase(RegisteredSubCommandBase):
    _registry = registry


class CreateEmobservationCommand(CreateChildBase):
    name = "emobservation"
    description = "Upload EM observation data to an event or superevent"
    parent_parsers = (object_id_parser,)

    def add_custom_arguments(self, parser):
        parser.add_argument("group", type=str,
            help=("Name of EM MOU group making the observation "
            "(do '{prog} show emgroups' to see options)".format(
            prog=self.base_prog)))
        parser.add_argument("ra_list", type=str, help=("Comma-separated list "
            "of right ascension coordinates (deg.)"))
        parser.add_argument("ra_width_list", type=str,
            help=("Comma-separated list of right ascension measurement widths "
            " OR a single number if all measurements have the same width "
            "(deg.)"))
        parser.add_argument("dec_list", type=str, help=("Comma-separated list "
            "of declination coordinates (deg.)"))
        parser.add_argument("dec_width_list", type=str,
            help=("Comma-separated list of declination measurement widths "
            " OR a single number if all measurements have the same width "
            "(deg.)"))
        parser.add_argument("start_time_list", type=str,
            help=("Comma-separated list of measurement start times in ISO "
            "8601 format"))
        parser.add_argument("duration_list", type=str,
            help=("List of exposure times OR a single number if all "
            "measurements have the same exposure (seconds)"))
        parser.add_argument("--comment", type=str,
            help="Comment about the observation")
        return parser

    def run(self, client, args):
        # Handle args that should be lists of floats
        ra_list = parse_delimited_string(args.ra_list, cast=float)
        dec_list = parse_delimited_string(args.dec_list, cast=float)

        # Split start times
        start_time_list = parse_delimited_string(args.start_time_list)

        # These can be either lists of floats or single floats
        list_or_num = lambda l: l if len(l) > 1 else l[0]
        ra_width_list = parse_delimited_string_or_single(args.ra_width_list,
            cast=float)
        dec_width_list = parse_delimited_string_or_single(args.dec_width_list,
            cast=float)
        duration_list = parse_delimited_string_or_single(
            args.duration_list, cast=float)

        return client.writeEMObservation(args.object_id, args.group, ra_list,
            ra_width_list, dec_list, dec_width_list, start_time_list,
            duration_list, comment=args.comment)


class CreateEventCommand(CreateChildBase):
    name = "event"
    description = "Create an event"
    parent_parsers = (label_parser,)

    def add_custom_arguments(self, parser):
        parser.add_argument("group", type=str,
            help=("Analysis group which identified the event "
            "(do '{prog} show groups' to see options)".format(
            prog=self.base_prog)))
        parser.add_argument("pipeline", type=str,
            help=("Analysis pipeline which identified the event "
            "(do '{prog} show pipelines' to see options)".format(
            prog=self.base_prog)))
        parser.add_argument("event_file", type=str, help="Event data file")
        parser.add_argument("search", type=str, nargs='?',
            help=("Search type (do '{prog} show searches' to see "
            "options)").format(prog=self.base_prog))
        parser.add_argument("--offline", action="store_true", default=False,
            help="Signifies that the event was found by an offline analysis")
        return parser

    def run(self, client, args):
        # Process labels arg, which can be a single label or a
        # comma-separated list of labels
        labels = parse_delimited_string_or_single(args.labels)

        # Handle case where user reverses order of search and event file
        # We don't print a warning (for now) since this is mimicing
        # legacy behavior
        event_file = args.event_file
        search = args.search
        if event_file in client.searches and os.path.isfile(search):
             temp = event_file
             event_file = search
             search = temp

        return client.createEvent(args.group, args.pipeline, event_file,
            search=search, offline=args.offline, labels=labels)


class CreateLogCommand(CreateChildBase):
    name = "log"
    description = "Create a log entry, with optional file upload"
    parent_parsers = (object_id_parser, comment_parser, tag_parser,)

    def add_custom_arguments(self, parser):
        parser.add_argument("filename", type=str, nargs='?',
            help="Path to file to be uploaded (optional)")
        return parser

    def run(self, client, args):
        # Parse args
        tag_name = parse_delimited_string_or_single(args.tag_name)
        tag_display_name = parse_delimited_string_or_single(
            args.tag_display_name)

        return client.writeLog(args.object_id, args.comment,
            filename=args.filename, tag_name=tag_name,
            displayName=tag_display_name)


class CreateSignoffCommand(CreateChildBase):
    name = "signoff"
    description = textwrap.dedent("""\
        Create an operator or advocate signoff. Only allowed for superevents
        which are labeled with the corresponding *OPS or ADVREQ labels.
        Event signoff creation is not presently implemented.
    """)
    parent_parsers = (superevent_id_parser,)

    def add_custom_arguments(self, parser):
        parser.add_argument("signoff_type", type=str,
            help=("Signoff type (do '{prog} show signoff_types') to see "
            "options").format(prog=self.base_prog))
        parser.add_argument("signoff_status", type=str,
            help=("Signoff type (do '{prog} show signoff_statuses') to see "
            "options").format(prog=self.base_prog))
        parser.add_argument("comment", type=str,
            help="Justification for signoff status")
        parser.add_argument("instrument", type=str, nargs='?',
            help=("Instrument code (do {prog} show instruments to see "
            "options). Required for operator signoffs.").format(
            prog=self.base_prog))
        return parser

    def run(self, client, args):
        instrument = args.instrument or '' # Convert None to ''
        return client.create_signoff(args.superevent_id, args.signoff_type,
            args.signoff_status, args.comment, instrument=instrument)


class CreateSupereventCommand(CreateChildBase):
    name = "superevent"
    description = "Create a superevent"
    parent_parsers = (label_parser,)

    def add_custom_arguments(self, parser):
        parser.add_argument("t_start", type=float,
            help="t_start of superevent")
        parser.add_argument("t_0", type=float, help="t_0 of superevent")
        parser.add_argument("t_end", type=float, help="t_end of superevent")
        parser.add_argument("preferred_event", type=str,
            help="Graceid of the preferred event")
        parser.add_argument("--category", type=str, default="production",
            help=("Superevent category (do '{prog} show superevent_categories "
            "to see options'").format(prog=self.base_prog))
        parser.add_argument("--events", type=str,
            help=("Comma-separated list of graceids corresponding to events "
            "which should be added to this superevent"))

        return parser

    def run(self, client, args):
        # Parse args which can be lists or single items
        labels = parse_delimited_string_or_single(args.labels)
        events = parse_delimited_string_or_single(args.events)

        return client.createSuperevent(args.t_start, args.t_0, args.t_end,
            args.preferred_event, category=args.category, events=events,
            labels=labels)


class CreateVoeventCommand(CreateChildBase):
    name = "voevent"
    description = "Create a VOEvent for an event or superevent"
    parent_parsers = (object_id_parser,)

    def add_custom_arguments(self, parser):
        parser.add_argument("voevent_type", type=str,
            help=("VOEvent type (do '{prog} show voevent_types to"
            "see options'").format(prog=self.base_prog))
        parser.add_argument("--skymap-type", type=str,
            help="Skymap type (required for VOEvents which include a skymap)")
        parser.add_argument("--skymap-filename", type=str,
            help=("Name of skymap file on the server (required for initial "
            "and update alerts, optional for preliminary)"))
        parser.add_argument("--external", action='store_true',
            default=False, help=("Signifies that the VOEvent should be "
            "distributed outside the LVC"))
        parser.add_argument("--open-alert", action='store_true',
            default=False, help=("Signifies that the candidate is an open "
            "alert"))
        parser.add_argument("--hardware-inj", action='store_true',
            default=False, help="The candidate is a hardware injection")
        parser.add_argument("--coinc-comment", action='store_true',
            default=False, help="The candidate has a possible counterpart GRB")
        parser.add_argument("--prob-has-ns", type=float, default=None,
            help=("Probability that one object in the binary has mass less "
            "than 3 M_sun (0.0 - 1.0)"))
        parser.add_argument("--prob-has-remnant", type=float, default=None,
            help=("Probability that there is matter in the surroundings of "
            "the central object (0.0 - 1.0)"))
        parser.add_argument("--bns", type=float, default=None,
            help=("Probability that the source is a binary neutron star "
            "merger (0.0 - 1.0)"))
        parser.add_argument("--nsbh", type=float, default=None,
            help=("Probability that the source is a neutron star-black hole "
            "merger (0.0 - 1.0)"))
        parser.add_argument("--bbh", type=float, default=None,
            help=("Probability that the source is a binary black hole "
            "merger (0.0 - 1.0)"))
        parser.add_argument("--terrestrial", type=float, default=None,
            help="Probability that the source is terrestrial (0.0 - 1.0)")
        parser.add_argument("--mass-gap", type=float, default=None,
            help=("Probability that at least one object in the binary is "
            "between 3 and 5 solar masses"))
        return parser

    def run(self, client, args):
        return client.createVOEvent(args.object_id, args.voevent_type,
            skymap_type=args.skymap_type, skymap_filename=args.skymap_filename,
            internal=(not args.external), open_alert=args.open_alert,
            hardware_inj=args.hardware_inj, CoincComment=args.coinc_comment,
            ProbHasNS=args.prob_has_ns, ProbHasRemnant=args.prob_has_remnant,
            BNS=args.bns, NSBH=args.nsbh, BBH=args.bbh,
            Terrestrial=args.terrestrial, MassGap=args.mass_gap)
