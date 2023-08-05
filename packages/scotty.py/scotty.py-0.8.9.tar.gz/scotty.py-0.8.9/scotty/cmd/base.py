from collections import defaultdict


class CommandRegistry(object):
    """Registry class for CLI commands."""

    registry = defaultdict(dict)

    @classmethod
    def parser(cls, parser_class):
        """Return decorator for an customized parser."""
        module_ = parser_class.__module__
        key = cls.getcommandkey(module_)
        cls.registry[key]['parser'] = parser_class
        return parser_class

    @classmethod
    def command(cls, command_class):
        """Return decorator for an customized command."""
        module_ = command_class.__module__
        key = cls.getcommandkey(module_)
        cls.registry[key]['command'] = command_class
        return command_class

    @classmethod
    def getcommandkey(cls, module_):
        """Create an identifier for the command based on the module."""
        key = module_.rsplit('.', 1)[-1]
        return key

    @classmethod
    def getbuilder(cls, command):
        """Determine the command builder based on the command."""
        builder_class = cls.registry[command].get('builder', CommandBuilder)
        return builder_class()

    @classmethod
    def getparser(cls, command):
        """Determine the command parser based on the command."""
        parser_class = cls.registry[command].get('parser', CommandParser)
        return parser_class()

    @classmethod
    def getcommand_class(cls, command):
        """Determine the command class based on the command."""
        return cls.registry[command]['command']


class CommandParser(object):
    """Abstract class for an CLI command parser."""

    def add_arguments(self, parser):
        """Interface to add new arguments to the CLI command."""
        raise NotImplementedError(
            'You must implement CommandParser.add_arguments(self, parser)')


class CommandBuilder(object):
    """This class represents an Builder for CLI commands."""

    def build_command(self, options, command_class):
        """Build command from options and command class."""
        command = command_class(options)
        return command
