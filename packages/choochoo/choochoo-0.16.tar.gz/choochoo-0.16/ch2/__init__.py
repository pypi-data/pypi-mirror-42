
from logging import getLogger, NullHandler
from sys import version_info

getLogger('bokeh').addHandler(NullHandler())
getLogger('tornado').addHandler(NullHandler())

from .command.activities import activities
from .command.args import COMMAND, parser, NamespaceWithVariables, PROGNAME, HELP, DEV, DIARY, FIT, \
    PACKAGE_FIT_PROFILE, ACTIVITIES, NO_OP, DEFAULT_CONFIG, CONSTANTS, STATISTICS, TEST_SCHEDULE, MONITOR, GARMIN, \
    UNLOCK, DATA, FIX_FIT, CH2_VERSION
from .command.constants import constants
from .command.data import data
from .command.default_config import default_config
from .command.diary import diary
from .command.fit import fit
from .command.fix_fit import fix_fit
from .command.garmin import garmin
from .command.help import help, LengthFmt
from .command.monitor import monitor
from .command.package_fit_profile import package_fit_profile
from .command.statistics import statistics
from .command.test_schedule import test_schedule
from .command.unlock import unlock
from .lib.io import tui
from .lib.log import make_log
from .squeal.database import Database
from .squeal.tables.constant import SystemConstant
from .uranus.server import set_jupyter_args, stop_jupyter


@tui
def no_op(args, log, db):
    '''
## no-op

This is used internally when accessing data in JupyterState or configuring the system
at the command line.
    '''
    pass


COMMANDS = {ACTIVITIES: activities,
            CONSTANTS: constants,
            DATA: data,
            DEFAULT_CONFIG: default_config,
            DIARY: diary,
            FIT: fit,
            FIX_FIT: fix_fit,
            GARMIN: garmin,
            HELP: help,
            MONITOR: monitor,
            STATISTICS: statistics,
            NO_OP: no_op,
            PACKAGE_FIT_PROFILE: package_fit_profile,
            TEST_SCHEDULE: test_schedule,
            UNLOCK: unlock
            }


def main():
    p = parser()
    args = NamespaceWithVariables(p.parse_args())
    command_name = args[COMMAND] if COMMAND in args else None
    command = COMMANDS[command_name] if command_name in COMMANDS else None
    tui = command and hasattr(command, 'tui') and command.tui
    log = make_log(args, tui=tui)
    log.info('Version %s' % CH2_VERSION)
    if version_info < (3, 7):
        raise Exception('Please user Python 3.7 or more recent')
    db = Database(args, log)
    try:
        if db.is_empty() and (not command or command_name != DEFAULT_CONFIG):
            refuse_until_configured()
        else:
            if not command_name or command_name not in (UNLOCK, FIT, FIX_FIT, GARMIN, TEST_SCHEDULE):
                with db.session_context() as s:
                    SystemConstant.assert_unlocked(s)
            set_jupyter_args(log, args)
            try:
                if command:
                    command(args, log, db)
                else:
                    log.debug('If you are seeing the "No command given" error during development ' +
                              'you may have forgotten to set the command name via `set_defaults()`.')
                    raise Exception('No command given (try `ch2 help`)')
            finally:
                stop_jupyter(log)
    except KeyboardInterrupt:
        log.critical('User abort')
    except Exception as e:
        log.critical(e)
        log.info('See `%s %s` for available commands.' % (PROGNAME, HELP))
        log.info('Docs at http://andrewcooke.github.io/choochoo')
        if not args or args[DEV]:
            raise


def refuse_until_configured():
    LengthFmt().print_all('''
Welcome to Choochoo.

Before using the ch2 command you must configure the system.

Please see the documentation at http://andrewcooke.github.io/choochoo

To generate a default configuration use the command

    %s %s

NOTE: The default configuration is only an example.  Please see the docs
for more details.''' % (PROGNAME, DEFAULT_CONFIG))
