from __future__ import absolute_import
import argparse
import gcalcli
from gcalcli import utils
from gcalcli.deprecations import parser_allow_deprecated, DeprecatedStoreTrue
from gcalcli.printer import valid_color_name
from oauth2client import tools
import copy as _copy

DETAILS = ['all', 'calendar', 'location', 'length', 'reminders', 'description',
           'longurl', 'shorturl', 'url', 'attendees', 'email', 'attachments']

BOOL_DETAILS = ['calendar', 'location', 'length', 'reminders', 'description',
                'attendees', 'email', 'attachments']

PROGRAM_OPTIONS = {
        '--client-id': {'default': gcalcli.__API_CLIENT_ID__,
                        'type': str,
                        'help': 'API client_id'},
        '--client-secret': {'default': gcalcli.__API_CLIENT_SECRET__,
                            'type': str,
                            'help': 'API client_secret'},
        '--config-folder': {'default': None, 'type': str,
                            'help': 'Optional directory to load/store all ' +
                                    'configuration information'},
        '--noincluderc': {'action': 'store_false',
                          'dest': 'includeRc',
                          'help': 'Whether to include ~/.gcalclirc when ' +
                                  'using configFolder'},
        '--calendar': {'default': [], 'type': str, 'action': 'append',
                       'help': 'Which calendars to use'},
        '--default-calendar': {'default': [], 'type': str, 'action': 'append',
                               'dest': 'defaultCalendar',
                               'help': 'Optional default calendar to use if ' +
                                       'no --calendar options are given'},
        '--locale': {'default': '', 'type': str, 'help': 'System locale'},
        '--refresh': {'action': 'store_true', 'dest': 'refresh_cache',
                      'default': False,
                      'help': 'Delete and refresh cached data'},
        '--nocache': {'action': 'store_false', 'dest': 'use_cache',
                      'default': True,
                      'help': 'Execute command without using cache'},
        '--conky': {'action': 'store_true', 'default': False,
                    'help': 'Use Conky color codes'},
        '--nocolor': {'action': 'store_false', 'default': True,
                      'dest': 'color',
                      'help': 'Enable/Disable all color output'},
        '--lineart': {'default': 'fancy',
                      'choices': ['fancy', 'unicode', 'ascii'],
                      'help': 'Choose line art style for calendars: ' +
                              '"fancy": for VTcodes, "unicode" for ' +
                              'Unicode box drawing characters, "ascii" ' +
                              'for old-school plusses, hyphens and pipes.'}
        }


class DetailsAction(argparse._AppendAction):

    def __call__(self, parser, namespace, value, option_string=None):
        details = _copy.copy(getattr(namespace, self.dest, {}))

        if value == 'all':
            details = {d: True for d in BOOL_DETAILS}
        elif value in BOOL_DETAILS:
            details[value] = True
        elif value in ['shorturl', 'url']:
            details['url'] = 'short'
        elif value == 'longurl':
            details['url'] = 'long'

        setattr(namespace, self.dest, details)


def validwidth(value):
    ival = int(value)
    if ival < 10:
        raise argparse.ArgumentTypeError('Width must be a number >= 10')
    return ival


def validreminder(value):
    if not utils.parse_reminder(value):
        raise argparse.ArgumentTypeError(
                'Not a valid reminder string: %s' % value)
    else:
        return value


def get_details_parser():
    details_parser = argparse.ArgumentParser(add_help=False)
    details_parser.add_argument(
            '--details', default={}, action=DetailsAction,
            choices=DETAILS,
            help='Which parts to display, can be: ' + ', '.join(DETAILS))
    return details_parser


def get_output_parser(parents=[]):
    output_parser = argparse.ArgumentParser(add_help=False, parents=parents)
    output_parser.add_argument(
            '--tsv', action='store_true', dest='tsv', default=False,
            help='Use Tab Separated Value output')
    output_parser.add_argument(
            '--nostarted', action='store_true', dest='ignore_started',
            default=False, help='Hide events that have started')
    output_parser.add_argument(
            '--nodeclined', action='store_true', dest='ignore_declined',
            default=False, help='Hide events that have been declined')
    output_parser.add_argument(
            '--width', '-w', default=10, dest='cal_width', type=validwidth,
            help='Set output width')
    output_parser.add_argument(
            '--military', action='store_true', default=False,
            help='Use 24 hour display')
    output_parser.add_argument(
            '--override-color', action='store_true', default=False,
            help='Use overridden color for event')
    return output_parser


@parser_allow_deprecated(name='color')
def get_color_parser():
    color_parser = argparse.ArgumentParser(add_help=False)

    COLOR_PARSER_OPTIONS = [
        ('owner', 'cyan', 'Color for owned calendars'),
        ('writer', 'cyan', 'Color for writeable calendars'),
        ('reader', 'magenta', 'Color for read-only calendars'),
        ('freebusy', 'default', 'Color for free/busy calendars'),
        ('date', 'yellow', 'Color for the date'),
        ('now-marker', 'brightred', 'Color for the now marker'),
        ('border', 'white', 'Color of line borders'),
        ('title', 'brightyellow', 'Color of the agenda column titles'),
    ]

    for arg, color, msg in COLOR_PARSER_OPTIONS:
        arg = '--color-' + arg
        color_parser.add_argument(
            arg, default=color, type=valid_color_name, help=msg
        )

    return color_parser


@parser_allow_deprecated(name='remind')
def get_remind_parser():
    remind_parser = argparse.ArgumentParser(add_help=False)
    remind_parser.add_argument(
            '--reminder', default=[], type=validreminder, dest='reminders',
            action='append',
            help='Reminders in the form "TIME METH" or "TIME".  TIME '
            'is a number which may be followed by an optional '
            '"w", "d", "h", or "m" (meaning weeks, days, hours, '
            'minutes) and default to minutes.  METH is a string '
            '"popup", "email", or "sms" and defaults to popup.')
    remind_parser.add_argument(
            '--default-reminders', action='store_true',
            dest='default_reminders', default=False,
            help='If no --reminder is given, use the defaults.  If this is '
            'false, do not create any reminders.')
    return remind_parser


def get_cal_query_parser():
    cal_query_parser = argparse.ArgumentParser(add_help=False)
    cal_query_parser.add_argument('start', type=str, nargs='?')
    cal_query_parser.add_argument(
            '--monday', action='store_true', dest='cal_monday', default=False,
            help='Start the week on Monday')
    cal_query_parser.add_argument(
            '--noweekend', action='store_false', dest='cal_weekend',
            default=True,  help='Hide Saturday and Sunday')
    return cal_query_parser


def get_start_end_parser():
    se_parser = argparse.ArgumentParser(add_help=False)
    se_parser.add_argument('start', type=utils.get_time_from_str, nargs='?')
    se_parser.add_argument('end', type=utils.get_time_from_str, nargs='?')
    return se_parser


def get_search_parser():
    # requires search text, optional start and end filters
    search_parser = argparse.ArgumentParser(add_help=False)
    search_parser.add_argument('text', nargs=1, type=utils._u)
    search_parser.add_argument(
            'start', type=utils.get_time_from_str, nargs='?')
    search_parser.add_argument('end', type=utils.get_time_from_str, nargs='?')
    return search_parser


def handle_unparsed(unparsed, namespace):
    # Attempt a reparse against the program options.
    # Provides some robustness for misplaced global options

    # make a new parser with only the global opts
    parser = argparse.ArgumentParser()
    for option, definition in PROGRAM_OPTIONS.items():
        parser.add_argument(option, **definition)

    return parser.parse_args(unparsed, namespace=namespace)


@parser_allow_deprecated(name='program')
def get_argument_parser():
    parser = argparse.ArgumentParser(
            description='Google Calendar Command Line Interface',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            fromfile_prefix_chars='@',
            parents=[tools.argparser])

    parser.add_argument(
            '--version', action='version', version='%%(prog)s %s (%s)' %
            (gcalcli.__version__, gcalcli.__author__))

    # Program level options
    for option, definition in PROGRAM_OPTIONS.items():
        parser.add_argument(option, **definition)

    # parent parser types used for subcommands
    details_parser = get_details_parser()
    color_parser = get_color_parser()

    # Output parser should imply color parser
    output_parser = get_output_parser(parents=[color_parser])

    remind_parser = get_remind_parser()
    cal_query_parser = get_cal_query_parser()

    # parsed start and end times
    start_end_parser = get_start_end_parser()

    # tacks on search text
    search_parser = get_search_parser()

    sub = parser.add_subparsers(
            help='Invoking a subcommand with --help prints subcommand usage.',
            dest='command')
    sub.required = True

    sub.add_parser(
            'list', parents=[color_parser], help='list available calendars',
            description='List available calendars.')

    sub.add_parser(
            'search', parents=[details_parser, output_parser, search_parser],
            help='search for events within an optional time period',
            description='Provides case insenstive search for calendar events.')
    sub.add_parser(
            'edit', parents=[details_parser, output_parser, search_parser],
            help='edit calendar events',
            description='Case insensitive search for items to find and edit '
            'interactively.')

    delete = sub.add_parser(
            'delete', parents=[output_parser, search_parser],
            help='delete events from the calendar',
            description='Case insensitive search for items to delete '
            'interactively.')
    delete.add_argument(
            '--iamaexpert', action='store_true', help='Probably not')

    sub.add_parser(
            'agenda',
            parents=[details_parser, output_parser, start_end_parser],
            help='get an agenda for a time period',
            description='Get an agenda for a time period.')

    calw = sub.add_parser(
            'calw', parents=[details_parser, output_parser, cal_query_parser],
            help='get a week-based agenda in calendar format',
            description='Get a week-based agenda in calendar format.')
    calw.add_argument('weeks', type=int, default=1, nargs='?')

    sub.add_parser(
            'calm', parents=[details_parser, output_parser, cal_query_parser],
            help='get a month agenda in calendar format',
            description='Get a month agenda in calendar format.')

    quick = sub.add_parser(
            'quick', parents=[details_parser, remind_parser],
            help='quick-add an event to a calendar',
            description='`quick-add\' an event to a calendar. A single '
            '--calendar must be specified.')
    quick.add_argument('text')

    add = sub.add_parser(
            'add', parents=[details_parser, remind_parser],
            help='add a detailed event to the calendar',
            description='Add an event to the calendar. Some or all metadata '
            'can be passed as options (see optional arguments).  If '
            'incomplete, will drop to an interactive prompt requesting '
            'remaining data.')
    add.add_argument(
            '--color',
            dest='event_color',
            default=None, type=str,
            help='Color of event in browser (overrides default). Choose '
                 'from lavender, sage, grape, flamingo, banana, tangerine, '
                 'peacock, graphite, blueberry, basil, tomato.'
    )
    add.add_argument('--title', default=None, type=str, help='Event title')
    add.add_argument(
            '--who', default=[], type=str, action='append', help='Event title')
    add.add_argument('--where', default=None, type=str, help='Event location')
    add.add_argument('--when', default=None, type=str, help='Event time')
    add.add_argument(
            '--duration', default=None, type=int,
            help='Event duration in minutes or days if --allday is given.')
    add.add_argument(
            '--description', default=None, type=str, help='Event description')
    add.add_argument(
            '--allday', action='store_true', dest='allday', default=False,
            help='If --allday is given, the event will be an all-day event '
            '(possibly multi-day if --duration is greater than 1). The '
            'time part of the --when will be ignored.')
    add.add_argument(
            '--noprompt', action='store_false', dest='prompt', default=True,
            help='Don\'t prompt for missing data when adding events')

    _import = sub.add_parser(
            'import', parents=[remind_parser],
            help='import an ics/vcal file to a calendar',
            description='Import from an ics/vcal file; a single --calendar '
            'must be specified.  Reads from stdin when no file argument is '
            'provided.')
    _import.add_argument(
            'file', type=argparse.FileType('r'), nargs='?', default=None)
    _import.add_argument(
            '--verbose', '-v', action='count', help='Be verbose on imports')
    _import.add_argument(
            '--dump', '-d', action='store_true',
            help='Print events and don\'t import')

    default_cmd = 'notify-send -u critical -i appointment-soon -a gcalcli %s'
    remind = sub.add_parser(
            'remind',
            help='execute command if event occurs within <mins> time',
            description='Execute <cmd> if event occurs within <mins>; the %s '
            'in <command> is replaced with event start time and title text.'
            'default command: "' + default_cmd + '"')
    remind.add_argument('minutes', nargs='?', type=int, default=10)
    remind.add_argument('cmd', nargs='?', type=str, default=default_cmd)

    remind.add_argument(
            '--use-reminders', action='store_true',
            help='Honor the remind time when running remind command')

    remind.add_argument(
            '--use_reminders', action=DeprecatedStoreTrue,
            help=argparse.SUPPRESS)

    return parser
