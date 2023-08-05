import contextlib
import os
import shutil
import unittest

from scotty import cli


class PerformExperimentTest(unittest.TestCase):
    """Testclass for experiment workflow."""

    cli_cmd = 'scotty experiment perform'
    test_script_name = os.path.basename(__file__)
    test_script_name = os.path.splitext(test_script_name)[0]
    experiment_samples_path = 'samples/components/experiment/single_workload'
    experiment_tmp_path_root = os.path.join('tmp', test_script_name)
    experiment_tmp_path = os.path.join(experiment_tmp_path_root, experiment_samples_path)

    def setUp(self):
        """Run setup test environment for experiment workflow."""
        if os.path.isdir(self.experiment_tmp_path):
            shutil.rmtree(self.experiment_tmp_path)
        shutil.copytree(self.experiment_samples_path, self.experiment_tmp_path)
        self.experiment_scotty_path = os.path.join(self.experiment_tmp_path, '.scotty/')
        self.set_up_workload_module_path()
        self.set_up_resource_module_path()

    def set_up_workload_module_path(self):
        """Run setup module path for demo workload."""
        self.workload_module_path = os.path.join(
            self.experiment_scotty_path,
            'components/workload/demo_workload/workload_gen.py')

    def set_up_resource_module_path(self):
        """Run setup module path for demo resource."""
        self.resource_module_path = os.path.join(
            self.experiment_scotty_path,
            'components/resource/demo_resource/resource_gen.py')

    def tearDown(self):
        """Delete experiment artefacts."""
        shutil.rmtree(self.experiment_tmp_path_root)

    def test_perform_experiment(self):
        """Test perform experiment workflow."""
        self._run_cmd()
        self.assertTrue(os.path.isdir(self.experiment_scotty_path), 'Missing .scotty directory')
        self.assertTrue(os.path.exists(self.workload_module_path), 'Missing demo_workload module')
        self.assertTrue(os.path.exists(self.resource_module_path), 'Missing demo_resource module')
        # check resource result
        # check workload result

    @contextlib.contextmanager
    def _cwd(self, path):
        prev_cwd = os.getcwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(prev_cwd)

    def _run_cmd(self):
        with self._cwd(self.experiment_tmp_path):
            cmd_args = self.cli_cmd.split(' ')
            cli.run(cmd_args)
