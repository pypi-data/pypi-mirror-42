import logging

from scotty.cmd.base import CommandParser
from scotty.cmd.base import CommandRegistry
from scotty.workflows.experiment import ExperimentCleanWorkflow
from scotty.workflows.experiment import ExperimentPerformWorkflow

logger = logging.getLogger(__name__)


@CommandRegistry.parser
class ExperimentParser(CommandParser):
    """Parser for experiment."""

    def add_arguments(self, parser):
        """Add new arguments to parser."""
        subparsers = parser.add_subparsers(
            help='Action',
            dest='action')
        subparsers.required = True
        performparser = subparsers.add_parser('perform')
        PerformParser().add_arguments(performparser)
        cleanparser = subparsers.add_parser('clean')
        CleanParser().add_arguments(cleanparser)


class CleanParser(CommandParser):
    """Parser for experiment clean."""

    def add_arguments(self, parser):
        """Add new arguments to parser."""
        parser.add_argument(
            '-w', '--workspace',
            help='Path to experiment workspace',
            dest='workspace',
            action='store',
            default='./')


class PerformParser(CommandParser):
    """Parser for experiment perform."""

    def add_arguments(self, parser):
        """Add new argument to parser."""
        parser.add_argument(
            '-w', '--workspace',
            help='Path to experiment workspace',
            dest='workspace',
            action='store',
            default='./')
        parser.add_argument(
            '-c', '--config',
            help='Path to experiment config',
            dest='config',
            action='store',
            default=None)
        parser.add_argument(
            '-m', '--mock',
            help='Do not run the workloads',
            dest='mock',
            default=False,
            action='store_true')


@CommandRegistry.command
class Command(object):
    """Command for experiment."""

    def __init__(self, options):
        """Bind experiment command to options."""
        self.options = options

    def execute(self):
        """Run commands for experiments."""
        if self.options.action == 'perform':
            workflow = ExperimentPerformWorkflow(self.options)
            workflow.run()
        elif self.options.action == 'clean':
            workflow = ExperimentCleanWorkflow(self.options)
            workflow.run()
