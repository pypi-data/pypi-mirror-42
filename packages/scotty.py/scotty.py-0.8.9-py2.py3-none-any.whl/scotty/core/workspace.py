import contextlib
import logging
import os

from scotty.core.exceptions import ExperimentException

logger = logging.getLogger(__name__)


class Workspace(object):
    """Basedatamodel for component workspaces."""

    def __init__(self, path):
        """Bind workspace to path."""
        self.path = os.path.abspath(path)
        self._config_path = None

    @property
    def config_path(self):
        """Return config path in workspace."""
        return self._config_path

    @config_path.setter
    def config_path(self, path):
        self._config_path = path

    @contextlib.contextmanager
    def cwd(self):
        """Change base dir temporally."""
        prev_cwd = os.getcwd()
        os.chdir(self.path)
        yield
        os.chdir(prev_cwd)

    @classmethod
    def factory(cls, component, workspace_path, create_paths=False):
        """Build workspace datamodel for component."""
        if component.isinstance('Workload'):
            workspace = WorkloadWorkspace(workspace_path)
        elif component.isinstance('Resource'):
            workspace = ResourceWorkspace(workspace_path)
        elif component.isinstance('SystemCollector'):
            workspace = SystemCollectorWorkspace(workspace_path)
        elif component.isinstance('Experiment'):
            workspace = ExperimentWorkspace(workspace_path)
        elif component.isinstance('ResultStore'):
            workspace = ResultStoreWorkspace(workspace_path)
        else:
            raise ExperimentException('Component {} is not supported'.format(type(component)))
        if create_paths:
            workspace.create_paths()
        return workspace


class ExperimentWorkspace(Workspace):
    """Datamodel for experiment workspace."""

    supported_components = [
        "resource",
        "systemcollector",
        "workload",
        "resultstore"
    ]

    data_components = [
        "workload",
    ]

    @property
    def config_path(self):
        """Return config path for experiment."""
        if not self._config_path:
            path = os.path.join(self.path, 'experiment.yaml')
            if not os.path.isfile(path):
                path = os.path.join(self.path, 'experiment.yml')
            self._config_path = path
        if not os.path.isfile(self._config_path):
            raise ExperimentException('Could not find the experiment config file.')
        return self._config_path

    @config_path.setter
    def config_path(self, path):
        """Set config path for experiment."""
        self._config_path = path

    def create_paths(self):
        """Prepare paths for components."""
        self.create_base_paths()
        self.component_path = {}
        self.component_data_path = {}
        for component in self.supported_components:
            self.create_component_path(component)
        for component in self.data_components:
            self.create_component_data_path(component)

    def create_base_paths(self):
        """Create base path for components in .scotty."""
        self.scotty_path = os.path.join(self.path, '.scotty')
        self.components_base_path = os.path.join(self.scotty_path, 'components')
        self.components_data_base_path = os.path.join(self.scotty_path, 'data')
        self.create_path(self.scotty_path)
        self.create_path(self.components_base_path)
        self.create_path(self.components_data_base_path)

    def create_component_path(self, component_type):
        """Create new path for component."""
        component_path = os.path.join(self.components_base_path, component_type)
        self.create_path(component_path)
        self.component_path[component_type] = component_path

    def create_component_data_path(self, component_type):
        """Create new data path for component."""
        component_data_path = os.path.join(self.components_data_base_path, component_type)
        self.create_path(component_data_path)
        self.component_data_path[component_type] = component_data_path

    def create_path(self, path):
        """Create new path."""
        if not os.path.isdir(path):
            os.mkdir(path)

    def get_component_path(self, component, create_on_demand=False):
        """Return path to component."""
        if component.type in self.supported_components:
            path = os.path.join(self.component_path[component.type], component.name)
            if create_on_demand:
                self.create_path(path)
            return path
        else:
            msg = 'Component {} is not supported'
            raise ExperimentException(msg.format(type(component)))

    def get_component_data_path(self, component, create_on_demand=False):
        """Return data path for component."""
        if component.type in self.data_components:
            path = os.path.join(self.component_data_path[component.type], component.name)
            if create_on_demand:
                self.create_path(path)
            return path
        else:
            msg = 'Component {} is not supported for data'
            raise ExperimentException(msg.format(type(component)))


class WorkloadWorkspace(Workspace):
    """Implementation for workload workspace."""

    pass


class ResourceWorkspace(Workspace):
    """Implementation for resource workspace."""

    pass


class SystemCollectorWorkspace(Workspace):
    """Implementation for systemcollector workspace."""

    pass


class ResultStoreWorkspace(Workspace):
    """Implementation for resultstore workspace."""

    pass
