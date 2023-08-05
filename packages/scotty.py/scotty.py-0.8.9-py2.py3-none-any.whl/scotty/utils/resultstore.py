import logging
import os

from scotty.utils.base import BaseUtils

logger = logging.getLogger(__name__)


class ResultstoreUtils(BaseUtils):
    """Utils for resultstore component."""

    def __init__(self, context):
        """Initialize resource utils and bind to an context."""
        try:
            self.current_resultstore = context.v1.resultstore
        except KeyError:
            logger.error('ResultStoreUtils can only used in resultstore context')
            raise

    @property
    def workloads(self):
        """Return list of current workloads from experiment."""
        workloads = self._BaseUtils__experiment.components['workload']
        return workloads

    @property
    def remote_base_dir(self):
        """Return basedirectory for scotty on remote resultstore."""
        return "scotty"

    @property
    def remote_experiment_dir(self):
        """Return experiment directory path on remote resultstore."""
        remote_experiment_dir = os.path.join(self.remote_base_dir, str(self.experiment_uuid))
        return remote_experiment_dir

    def local_result_dir(self, workload_name):
        """Return local resultstore for given workload."""
        local_result_dir = os.path.join('.scotty/data/workload', workload_name)
        return local_result_dir
