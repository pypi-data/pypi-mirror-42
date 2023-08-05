import unittest
from concurrent.futures import wait as futures_wait

import mock

from scotty.core.executor import ComponentExecutor
from scotty.core.executor import ResourceDeployExecutor
from scotty.core.executor import WorkloadRunExecutor


class ComponentExecutorTest(unittest.TestCase):
    """Testclass for component executor."""

    @mock.patch('scotty.core.executor.exec_component')
    def test_submit_execute(self, exec_component_mock):
        """Run test for executor submit."""
        self.skipTest("Can not tested yet because of Can't pickle <class 'mock.mock.MagicMock'>")
        exec_component_mock.__reduce__ = lambda self: (mock.MagicMock, ())
        component_executor = ComponentExecutor()
        component_executor.submit(
            'experiment',
            'component',
            'interface_',
            result_interface="result")
        futures_wait(component_executor._future_to_component)
        exec_component_mock.assert_called()

    def test__get_function(self):  # , getattr_mock):
        """Run test for get function."""
        pass


class WorkloadExecutorTest(unittest.TestCase):
    """Testclass for workload executor."""

    @mock.patch('scotty.core.executor.ComponentExecutor.submit')
    @mock.patch('scotty.core.components.Experiment')
    def test_submit_workloads(self, experiment_mock, submit_mock):
        """Run test for workload submit."""
        workloads_mock = {}
        workloads_mock['workload_1'] = mock.Mock()
        workloads_mock['workload_2'] = mock.Mock()
        experiment_mock.components = {}
        experiment_mock.components['workload'] = workloads_mock
        workload_run_executor = WorkloadRunExecutor(experiment_mock)
        workload_run_executor.submit_components()
        submit_mock.assert_called()

    def test_collect_results(self):
        """Run test for collect results."""
        pass


class ResourceDeployExecutorTest(unittest.TestCase):
    """Testclass for resource deployment executor."""

    @mock.patch('scotty.core.executor.ComponentExecutor.submit')
    @mock.patch('scotty.core.components.Experiment')
    def test_submit_resources(self, experiment_mock, submit_mock):
        """Run test for resource submit."""
        resources_mock = {}
        resources_mock['resource_1'] = mock.Mock()
        resources_mock['resource_2'] = mock.Mock()
        experiment_mock.components = {}
        experiment_mock.components['resource'] = resources_mock
        resource_deploy_executor = ResourceDeployExecutor(experiment_mock)
        resource_deploy_executor.submit_components()
        submit_mock.assert_called()
