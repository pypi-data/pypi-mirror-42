import logging

logger = logging.getLogger(__name__)


class Workflow(object):
    """Base class for workflows."""

    def __init__(self, options):
        """Initialize workflow object and set options."""
        self._options = options

    def run(self):
        """Run prepare, run and clean for a workflow."""
        self._prepare()
        self._run()
        self._clean()

    def _prepare(self):
        msg = '_prepare(self) must be implemented'
        raise NotImplementedError(msg)

    def _run(self):
        msg = '_run(self) must be implemented'
        raise NotImplementedError(msg)

    def _clean(self):
        msg = '_clean(self) must be implemented'
        raise NotImplementedError(msg)
