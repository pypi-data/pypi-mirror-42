import logging
from enum import Enum

from scotty.cmd.base import CommandParser
from scotty.cmd.base import CommandRegistry
from scotty.core.exceptions import ScottyException
from scotty.workflows.workflows import WorkloadInitWorkflow

logger = logging.getLogger(__name__)


class CommandAction(Enum):
    """Datamodel for workload command actions."""

    init = "init"


@CommandRegistry.parser
class WorkloadParser(CommandParser):
    """Parser for workload."""

    def add_arguments(self, parser):
        """Add arguments to parser."""
        subparsers = parser.add_subparsers(
            help='Action',
            dest='action')
        initparser = subparsers.add_parser(CommandAction.init.name)
        InitParser().add_arguments(initparser)


class InitParser(CommandParser):
    """Parser for workload init."""

    def add_arguments(self, parser):
        """Add arguments to parser."""
        parser.add_argument(
            'directory',
            nargs='?',
            metavar='directory',
            type=str,
            help="Directory where the workload repo will be created (Default:'./')",
            default='./')


@CommandRegistry.command
class Command(object):
    """Workload commands."""

    def __init__(self, options):
        """Bind workload command to options."""
        self.options = options

    def execute(self):
        """Run commands for workload."""
        command_action = CommandAction(self.options.action)
        if command_action is CommandAction.init:
            try:
                workflow = WorkloadInitWorkflow(self.options)
                workflow.run()
            except ScottyException as err:
                logger.error(err)
