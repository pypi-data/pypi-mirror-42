import logging

from scotty.core.exceptions import ScottyException

logger = logging.getLogger(__name__)


class ContextAccessible(object):
    """Datamodel for context component accessible."""

    accessibles = {}

    def __init__(self, component_type):
        """Bind context accessible to component type."""
        self.component_type = component_type.lower()
        if self.component_type not in ContextAccessible.accessibles:
            ContextAccessible.accessibles[self.component_type] = {}
        self.component_accessible = ContextAccessible.accessibles[self.component_type]

    def __call__(self, function_):
        """Set function accessible."""
        self.component_accessible[function_.__name__] = True
        return function_

    def setaccess(self, attribute_name):
        """Set accessible falg value for attribute."""
        self.component_accessible[attribute_name] = True

    def isaccessible(self, name):
        """Return accessible flag value for attribute."""
        return self.component_accessible.get(name, False)


class Context(object):
    """Basedatamodel for context."""

    def __init__(self, component, experiment):
        """Bind context to experiment and component."""
        self._context = {}
        self._context['v1'] = ContextV1(component, experiment)

    def __getattr__(self, version):
        """Return context depends on version."""
        return self._context[version]


class ContextV1(Context):
    """Datamodel for context version 1."""

    def __init__(self, component, experiment):
        """Bind context to component and experiment."""
        self._context = {}
        self._context[component.type] = ContextComponent(component)
        self.__experiment = experiment


class ContextComponent(Context):
    """Wrapperclass for component to hidde inaccessible attributes."""

    def __init__(self, component):
        """Bind context component to component."""
        self.__context_accessible = ContextAccessible(component.__class__.__name__)
        self.__component = component

    def __getattr__(self, name):
        """Run only accessible attributes on component."""
        if self.__context_accessible.isaccessible(name):
            return getattr(self.__component, name)
        else:
            raise ScottyException('{} not found'.format(name))
