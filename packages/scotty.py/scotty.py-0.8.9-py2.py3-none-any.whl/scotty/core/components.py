import logging
import os
import re
import sys
import uuid
from collections import defaultdict
from enum import Enum

from scotty.core import settings
from scotty.core.checkout import CheckoutManager
from scotty.core.context import ContextAccessible
from scotty.core.exceptions import ExperimentException
from scotty.core.exceptions import ScottyException
from scotty.core.moduleloader import ModuleLoader
from scotty.core.workspace import ExperimentWorkspace, Workspace

import yaml

logger = logging.getLogger(__name__)


class CommonComponentState(Enum):
    """Common states for components."""

    PREPARE = 0
    ACTIVE = 1
    COMPLETED = 2
    DELETED = 3
    ERROR = 4


class Component(object):
    """Component datamodel."""

    def __init__(self):
        """Prepare component datamodel."""
        self.uuid = uuid.uuid4()
        self.config = None
        self.workspace = None
        self.starttime = None
        self.endtime = None
        self._generator = None
        self._setaccess('uuid')
        self._setaccess('config')
        self._setaccess('name')
        self._setaccess('starttime')
        self._setaccess('endtime')
        self._setaccess('type')

    def _setaccess(self, parameter):
        ContextAccessible(self.__class__.__name__).setaccess(parameter)

    @property
    def name(self):
        """Return component name."""
        return self.config['name']

    def issource(self, type_):
        """Check source type."""
        source_type = self.get_source_type()
        same_type = source_type == type_.upper()
        return same_type

    def _parse_generator(self):
        """Parse component generator from config."""
        pattern_source_str = re.compile(r'(git|file):([^\[]+)(?:\[([^\]]+)\])?$')
        source_str = self.config['generator']
        groups = pattern_source_str.match(source_str).groups()
        self._generator = {
            "type": groups[0],
            "location": groups[1],
            "reference": groups[2]
        }

    @property
    def generator(self):
        """Return generator definition for component."""
        if not self._generator:
            self._parse_generator()
        return self._generator

    def get_source_type(self):
        """Return type of component source."""
        source = self.config['generator'].split(':')
        source_type = source[0].upper()
        return source_type

    def isinstance(self, type_str):
        """Check if component is instance of type."""
        class_ = getattr(sys.modules[__name__], type_str)
        return isinstance(self, class_)

    @property
    def type(self):
        """Return component type."""
        type_ = self.__class__.identifier()
        return type_

    @classmethod
    def identifier(cls, plural=False):
        """Return identifier for component."""
        identifier = cls.__name__
        if plural:
            identifier = "{}s".format(identifier)
        identifier = identifier.lower()
        return identifier

    @classmethod
    def factory(cls):
        """Return factory for component type."""
        component_factory_str = "{}Factory".format(cls.__name__)
        component_factory = getattr(sys.modules[__name__], component_factory_str)
        return component_factory


class WorkloadState(Enum):
    """States for workload component."""

    PREPARE = 0
    ACTIVE = 1
    COMPLETED = 2
    DELETED = 3
    ERROR = 4


class Workload(Component):
    """Datamodule for workload component."""

    module_interfaces = [
        'run',
    ]

    def __init__(self):
        """Prepare workload datamodel."""
        super(Workload, self).__init__()
        self.module = None
        self.parent_module_name = 'scotty.workload'
        self.state = WorkloadState.PREPARE
        self.result = None
        self._setaccess('params')
        self._setaccess('resources')
        self._setaccess('result')

    @property
    def module_path(self):
        """Return path to workload module file."""
        return os.path.join(self.workspace.path, 'workload_gen.py')

    @property
    def params(self):
        """Return workload parameter."""
        return self.config.get('params', [])

    @property
    def resources(self):
        """Return resources associated with workload."""
        return self.config.get('resources', [])


class Experiment(Component):
    """Datamodel for experiment component."""

    def __init__(self):
        """Prepare datamodel for experiment."""
        super(Experiment, self).__init__()
        self.components = defaultdict(dict)
        self.state = CommonComponentState.PREPARE

    def add_component(self, component):
        """Add new component to experiment."""
        if component.type in ExperimentWorkspace.supported_components:
            self.components[component.type][component.name] = component
        else:
            raise ExperimentException(
                'Component {} cannot add to experiment'.format(
                    component.type))

    def has_errors(self):
        """Return if experiment has errors."""
        return self.state == CommonComponentState.ERROR


class ResourceState(Enum):
    """States for resource components."""

    PREPARE = 0
    ACTIVE = 1
    COMPLETED = 2
    DELETED = 3
    ERROR = 4


class Resource(Component):
    """Datamodel for resource component."""

    module_interfaces = [
        'deploy',
        'clean',
        'exists',
        'endpoint'
    ]

    def __init__(self):
        """Prepare resource datamodel."""
        super(Resource, self).__init__()
        self.module = None
        self.parent_module_name = 'scotty.resource'
        self.state = CommonComponentState.PREPARE
        self.endpoint = None
        self._exists = None
        self._setaccess('params')
        self._setaccess('endpoint')

    @property
    def params(self):
        """Return resource parameters."""
        return self.config.get('params', [])

    @property
    def module_path(self):
        """Return module file path in resource workspace."""
        return os.path.join(self.workspace.path, 'resource_gen.py')

    @property
    def exists(self):
        """Return if resource exists on infrastructure and should reused."""
        if self._exists:
            if self.config.get('reuse', False):
                return True
            else:
                msg = 'Reuse flag for resource "{}" is not set but resource exists!'
                msg = msg.format(self.name)
                logger.error(msg)
                raise ScottyException(msg)

    @exists.setter
    def exists(self, exists):
        """Set resource exists on infrastructure."""
        self._exists = exists

    @property
    def keep(self):
        """Return if resource should keep on infrastructure."""
        return self.config.get('keep', False)


class SystemCollector(Component):
    """Datamodel for systemcollector component."""

    module_interfaces = [
        'collect',
    ]

    def __init__(self):
        """Prepare systemcollector datamodel."""
        super(SystemCollector, self).__init__()
        self.module = None
        self.parent_module_name = 'scotty.systemcollector'
        self.state = CommonComponentState.PREPARE
        self.result = None
        self._setaccess('result')

    @property
    def module_path(self):
        """Return path to module file in systemcollector workspace."""
        return os.path.join(self.workspace.path, 'systemcollector.py')


class ResultStore(Component):
    """Datamodel for resultstore component."""

    module_interfaces = [
        'submit',
    ]

    def __init__(self):
        """Prepare resultstore datamodel."""
        super(ResultStore, self).__init__()
        self.module = None
        self.parent_module_name = 'scotty.resultstore'
        self.state = CommonComponentState.PREPARE
        self._setaccess('params')

    @property
    def params(self):
        """Return resultstore parameter."""
        return self.config.get('params', [])

    @property
    def module_path(self):
        """Return path to module file in resultstore workspace."""
        return os.path.join(self.workspace.path, 'resultstore.py')


class ComponentValidator(object):
    """Validator for Component."""

    @classmethod
    def validate_interfaces(cls, component):
        """Check all interfaces on component."""
        pass
        for interface_ in component.module_interfaces:
            cls.validate_interface(component, interface_)

    @classmethod
    def validate_interface(cls, component, interface_):
        """Check if interface exists on component."""
        pass
        try:
            getattr(component.module, interface_)
        except AttributeError:
            err_msg = 'Missing interface {} for {} {}.'.format(
                interface_,
                component.type,
                component.name)
            raise ScottyException(err_msg)


class ComponentFactory(object):
    """Baseclass for component factories."""

    @classmethod
    def _get_component_workspace(cls, experiment, component):
        workspace_path = experiment.workspace.get_component_path(component)
        workspace = Workspace.factory(component, workspace_path)
        return workspace

    @classmethod
    def _get_component_module(cls, experiment, component):
        CheckoutManager.populate(component, experiment.workspace.path)
        module_ = ModuleLoader.load_by_component(component)
        return module_

    @classmethod
    def _build_from_experiment(cls, experiment, component_class):
        component_configs = experiment.config.get(component_class.identifier(True), [])
        component_factory = component_class.factory()
        components = [component_factory.build(config, experiment) for config in component_configs]
        return components


class ExperimentFactory(ComponentFactory):
    """Factory to build experiment."""

    yaml_pattern_env = re.compile(r'\<%=\s*ENV\[\'([^\]\s]+)\'\]\s*%\>')
    build_types = {
        'GIT': 'build_from_git',
        'WORKSPACE': 'build_from_workspace',
        'CONFIG': 'build_from_config',
    }

    @classmethod
    def build(cls, build_type='WORKSPACE', **params):
        """Build experient from build_type(WORKSPACE|CONFIG|GIT)."""
        build_function_name = cls.build_types.get(build_type, None)
        if build_function_name is None:
            error_msg = 'None supported build type {}'.format(build_type)
            raise ScottyException(error_msg)
        else:
            build_function = getattr(cls, build_function_name)
            return build_function(**params)

    @classmethod
    def build_from_git(cls, git_url, workspace_path, git_ref=None, cfg_path=None):
        """Build experiment from git source."""
        CheckoutManager.checkout(git_url, workspace_path, git_ref)
        cls.build_from_workspace(workspace_path, cfg_path)

    @classmethod
    def build_from_config(cls, workspace_path, experiment_cfg, data_cfg=None):
        """Build experiment from config."""
        # TODO create workspace
        # TODO create experiment.yaml in workspace
        # TODO copy data into workspace
        # TODO build from workspace
        pass

    @classmethod
    def build_from_workspace(cls, workspace_path, cfg_path=None):
        """Build experiment from workload_path."""
        experiment = Experiment()
        experiment.workspace = Workspace.factory(experiment, workspace_path, True)
        experiment.workspace.config_path = cls._get_experiment_config_path(experiment, cfg_path)
        experiment.config = cls._get_experiment_config(experiment)
        cls._build_components(experiment)
        return experiment

    @classmethod
    def _build_components(cls, experiment):
        components = cls._build_from_experiment(experiment, Resource)
        components += cls._build_from_experiment(experiment, Workload)
        components += cls._build_from_experiment(experiment, SystemCollector)
        components += ResultStoreFactory.build_from_settings(experiment)
        for component in components:
            experiment.add_component(component)

    @classmethod
    def _get_experiment_config_path(cls, experiment, config_path):
        config_path = config_path or experiment.workspace.config_path
        return config_path

    @classmethod
    def _get_experiment_config(cls, experiment):
        with open(experiment.workspace.config_path, 'r') as stream:
            yaml.add_implicit_resolver("!scotty_yaml_env", cls.yaml_pattern_env)
            yaml.add_constructor('!scotty_yaml_env', cls._scotty_yaml_env_constructor)
            config = yaml.load(stream)
        return config

    @classmethod
    def _scotty_yaml_env_constructor(cls, loader, node):
        value = loader.construct_scalar(node)
        env_var = cls.yaml_pattern_env.match(value).groups()[0]
        return os.environ.get(env_var, '')


class ResourceFactory(ComponentFactory):
    """Component factory for resources."""

    @classmethod
    def build(cls, resource_config, experiment):
        """Build resource component from resource config and experiment."""
        resource = Resource()
        resource.config = resource_config
        resource.workspace = cls._get_component_workspace(experiment, resource)
        return resource


class SystemCollectorFactory(ComponentFactory):
    """Component factory for systemcollectors."""

    @classmethod
    def build(cls, systemcollector_config, experiment):
        """Build systemcollector from config and experiment."""
        systemcollector = SystemCollector()
        systemcollector.config = systemcollector_config
        systemcollector.workspace = cls._get_component_workspace(experiment, systemcollector)
        return systemcollector


class WorkloadFactory(ComponentFactory):
    """Component factory for workloads."""

    @classmethod
    def build(cls, workload_config, experiment):
        """Build an workload component from experiment and workload config."""
        workload = Workload()
        workload.config = workload_config
        workload.workspace = cls._get_component_workspace(experiment, workload)
        return workload


class ResultStoreFactory(ComponentFactory):
    """Component factory for resultstore."""

    @classmethod
    def build(cls, resultstore_config, experiment):
        """Build an resultstore component from experiment and resultstore config."""
        resultstore = ResultStore()
        resultstore.config = resultstore_config
        resultstore.workspace = cls._get_component_workspace(experiment, resultstore)
        return resultstore

    @classmethod
    def build_from_settings(cls, experiment):
        """Build resultstore components from experiment settings."""
        resultstores = []
        setting_resultstores = settings.get('resultstores', 'stores')
        for setting_resultstore in setting_resultstores:
            enable = settings.get(setting_resultstore, 'enable')
            if not enable:
                continue
            resultstore_config = {}
            resultstore_config['name'] = setting_resultstore
            resultstore_config['generator'] = settings.get(setting_resultstore, 'generator')
            resultstore_config['params'] = settings.get(setting_resultstore, 'params')
            resultstore = cls.build(resultstore_config, experiment)
            resultstores.append(resultstore)
        return resultstores
