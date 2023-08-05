import logging
from enum import Enum

from scotty.cmd.base import CommandParser
from scotty.cmd.base import CommandRegistry
from scotty.core.exceptions import ScottyException
from scotty.workflows.resource import ResourceInitWorkflow

logger = logging.getLogger(__name__)


class CommandAction(Enum):
    """Datamodul for resource command actions."""

    init = 'init'


@CommandRegistry.parser
class ResourceParser(CommandParser):
    """Parser for resource."""

    def add_arguments(self, parser):
        """Add arguments to parser."""
        subparsers = parser.add_subparsers(help='Action', dest='action')
        initparser = subparsers.add_parser(CommandAction.init.name)
        InitParser().add_arguments(initparser)


class InitParser(CommandParser):
    """Parser for resource init."""

    def add_arguments(self, parser):
        """Add arguments to parser."""
        parser.add_argument(
            'name',
            metavar='name',
            type=str,
            help="Name for the resource")


@CommandRegistry.command
class Command(object):
    """Command for resources."""

    def __init__(self, options):
        """Bind resource command to options."""
        self.options = options

    def execute(self):
        """Run resource commands."""
        command_action = CommandAction(self.options.action)
        if command_action is CommandAction.init:
            try:
                workflow = ResourceInitWorkflow(self.options)
                workflow.run()
            except ScottyException as err:
                logger.error(err)
