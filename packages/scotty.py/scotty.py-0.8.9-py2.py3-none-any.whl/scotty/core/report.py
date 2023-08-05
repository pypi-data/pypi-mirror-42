import logging

logger = logging.getLogger(__name__)


class ReportCollector(object):
    """Datamodel for report collection."""

    def __init__(self, experiment):
        """Bind report collector to experiment."""
        self.experiment = experiment

    def collect_static(self):
        """Collect static report informations."""
        pass

    def collect(self):
        """Collect reports from componets."""
        pass

    def write_report(self):
        """Write report to result."""
        pass
