import unittest
import uuid

import mock

from scotty.core.components import Experiment
from scotty.utils.experiment import ExperimentUtils


class ExperimentUtilsTest(unittest.TestCase):
    """Testclass for ExprimentUtils."""

    @mock.patch('scotty.core.workspace.ExperimentWorkspace')
    @mock.patch('scotty.core.context.Context')
    def test_get_experiment_uuid(self, context_mock, exp_workspace_mock):
        """Run test for experiment uuid."""
        experiment = Experiment()
        experiment.workspace = exp_workspace_mock
        context_mock.v1._ContextV1__experiment = experiment
        experiment_utils = ExperimentUtils(context_mock)
        uuid = experiment_utils.experiment_uuid
        uuid_string = str(uuid)
        self.assertTrue(self.validate_uuid4(uuid_string))

    def validate_uuid4(self, uuid_string):
        """Run test for uuid creating."""
        try:
            uuid.UUID(uuid_string, version=4)
        except ValueError:
            return False
        return True
