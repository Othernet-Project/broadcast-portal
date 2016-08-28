import argparse

from ..cmdline import DummyCommand
from ..cmdline.version import Version
from ..cmdline.conf import Conf
from ..cmdline.process import Startup, Stop
from ..cmdline.custom_conf import CustomConf
from ..cmdline.custom_skin import CustomSkin
from ..cmdline.assets import Watch, StopWatchers, Recompile

from .exts import container as exts


OPTIONS = (
    Version,
    Conf,
    Startup,
)

COMMANDS = (
    Stop,
    CustomConf,
    CustomSkin,
    Watch,
    StopWatchers,
    Recompile,
)

COMMANDS_DICT = {c.name: c for c in COMMANDS}

DESCRIPTION = 'Filecast ceneter application manager and utility commands'


def cmdhelp():
    """
    Format the help section for the commands
    """
    longest_command = max([len(name) for name in COMMANDS_DICT.keys()])
    help = ['utility commands:']
    cmdformat = '  {:%s}  {}' % (longest_command,)
    for command in COMMANDS:
        help.append(cmdformat.format(command.name, command.help))
    return '\n'.join(help)


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('command', metavar='COMMAND', nargs='?',
                        help='optional utility command (use --help COMMAND '
                        'to get invididual command options)')

    # Register all options
    options = [option(parser) for option in OPTIONS]

    # Parse the option arguments and execute any options that need to be
    # executed according to their test method.
    args, remainder = parser.parse_known_args()
    for option in options:
        if option.test(args):
            option.run(args)

    if args.command:
        # Command was specified on the command line so select the appropriate
        # command class and use its help property as description.
        cmdclass = COMMANDS_DICT[args.command]
        description = cmdclass.help
        epilog = None
    else:
        # No command was specified: use dummy command class and use the help
        # text for all commands as description.
        cmdclass = DummyCommand
        description = 'start the application or run utility commands'
        epilog = cmdhelp()

    # Prepare for parsing commands
    parser = argparse.ArgumentParser(
        prog=exts.name, parents=[parser], description=description,
        epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    command = cmdclass(parser)
    args = parser.parse_args(remainder)
    command.run(args)
    return args
