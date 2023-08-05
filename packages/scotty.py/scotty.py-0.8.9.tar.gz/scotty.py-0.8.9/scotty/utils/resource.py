import logging
import os
from time import sleep

import heatclient.client
from heatclient.common import template_utils
from heatclient.exc import HTTPNotFound

import keystoneauth1.loading
import keystoneauth1.session
from keystoneauth1.exceptions.connection import ConnectFailure

from scotty.core import settings
from scotty.utils.base import BaseUtils

logger = logging.getLogger(__name__)


class ResourceUtils(BaseUtils):
    """Utils class for resources."""

    def _init(self, context):
        self._openstack = None
        try:
            self.current_resource = context.v1.resource
        except KeyError:
            logger.error('ResourceUtils can only used in reource context')
            raise

    def join_resource_path(self, path):
        """Return absolute resource path."""
        basepath = self.experiment_workspace.get_component_path(self.current_resource)
        return os.path.join(basepath, path)

    @property
    def openstack(self):
        """Return existing openstack client or create a new one."""
        if not self._openstack:
            self._openstack = OpenStack(self)
        return self._openstack


class OpenStack(object):
    """OpenStack class with heat client."""

    def __init__(self, resource_utils):
        """Init openstack."""
        self._session = None
        self._heat = None
        self._resource_utils = resource_utils

    @property
    def session(self):
        """Return an new session."""
        if not self._session:
            keystone_password_loader = keystoneauth1.loading.get_plugin_loader('password')
            auth = keystone_password_loader.load_from_options(
                auth_url=settings.get('openstack', 'auth_url'),
                username=settings.get('openstack', 'username'),
                user_domain_name=settings.get('openstack', 'user_domain_name'),
                password=settings.get('openstack', 'password'),
                project_name=settings.get('openstack', 'project_name'),
                project_domain_name=settings.get('openstack', 'project_domain_name')
            )
            self._session = keystoneauth1.session.Session(auth=auth)
        return self._session

    @property
    def heat(self):
        """Return existing heat client or create an new heat client."""
        if not self._heat:
            heatclient_ = heatclient.client.Client('1', session=self.session)
            self._heat = HeatWrapper(heatclient_)
        return self._heat

    def stack_exists(self, resource_name):
        """Check stack exists."""
        try:
            self.heat.stacks.get(resource_name)
        except HTTPNotFound:
            return False
        else:
            return True

    def deploy(self, resource_name, tpl_params, activate_collector=False):
        """Deploy stack with resource_name and template."""
        logger.debug('Start to deploy resource {} with parameters: {}'.format(
            resource_name, tpl_params))
        if activate_collector:
            tpl_params = self._inject_collector(tpl_params)
        tpl_args = self._heat_create_args(resource_name, tpl_params)
        self.heat.stacks.create(**tpl_args)
        self._wait_for_stack(resource_name)

    def destroy(self, resource_name):
        """Destroy stack in openstack."""
        self.heat.stacks.delete(resource_name)
        self._wait_for_stack(resource_name, state_finish="DELETE_COMPLETE",
                             state_error="DELETE_FAILED")

    def get_stack_outputs(self, resource_name):
        """Return outputs from heat resource stack as dict."""
        stack = self.heat.stacks.get(resource_name)
        outputs = self.parse_outputs(stack)
        return outputs

    def _heat_create_args(
        self,
        resource_name,
        tpl_params,
        tpl_rel_path='./templates/resource-stack.yaml'
    ):
        tpl_path = self._resource_utils.join_resource_path(tpl_rel_path)
        tpl_files, tpl = template_utils.get_template_contents(tpl_path)
        args = {
            'stack_name': resource_name,
            'template': tpl,
            'files': tpl_files,
            'parameters': tpl_params,
        }
        return args

    def _inject_collector(self, tpl_params):
        tpl_params['influx_db'] = settings.get('influxdb', 'database')
        tpl_params['influx_user'] = settings.get('influxdb', 'username')
        tpl_params['influx_passwd'] = settings.get('influxdb', 'password')
        tpl_params['influx_url'] = settings.get('influxdb', 'url')
        logger.debug('Template parameter: {}'.format(tpl_params))
        return tpl_params

    # TODO refactor based on HeatWrapper
    def _wait_for_stack(
        self,
        resource_name,
        state_finish="CREATE_COMPLETE",
        state_error="CREATE_FAILED"
    ):
        while True:
            info_msg = f'Wait for stack \'{resource_name}\' to reach the state \'{state_finish}\''
            logger.info(info_msg)
            try:
                stack = self.heat.stacks.get(resource_name)
            except Exception:
                if self._handle_wait_except(stack, state_finish, state_error):
                    break
            else:
                if self._handle_wait_else(stack, state_finish, state_error):
                    break
            sleep(10)

    def _handle_wait_except(self, stack, state_finish, state_error):
        if self._check_stack_status(stack, state_error):
            raise Exception(f'{stack.stack_name} failed while waiting for {state_finish}')
        if state_finish == "DELETE_COMPLETE":
            return True

    def _handle_wait_else(self, stack, state_finish, state_error):
        logger.info(f'Current stack status {stack.stack_status}')
        if self._check_stack_status(stack, state_error):
            raise Exception(f'{stack.stack_name} failed while waiting for {state_finish}')
        if self._check_stack_status(stack, state_finish):
            return True

    def _check_stack_status(self, stack, status):
        check = False
        if stack:
            check = stack.stack_status == status
        return check

    def parse_outputs(self, stack):
        """Return outputs from stack as dict."""
        outputs = {}
        for output in stack.outputs:
            outputs[output['output_key']] = output['output_value']
        return outputs


class HeatWrapper():
    """Wrapper class for heat client."""

    def __init__(self, heat):
        """Init heat wrapper with heat client."""
        self._heat = heat

    @property
    def stacks(self):
        """Return stacks object from heat."""
        return StacksWrapper(self._heat.stacks)


class StacksWrapper():
    """Wrapper class for heat stacks to use robust calls."""

    def __init__(self, stacks):
        """Init stack wrapper class with an heat stack."""
        self._stacks = stacks

    def get(self, resource_name):
        """Wrap stack get."""
        fn = self._stacks.get
        stack = self._robust_heat_call(fn, resource_name)
        return stack

    def _robust_heat_call(self, fn, *args, **kwargs):
        retries = 5
        while retries > 0:
            retries -= 1
            try:
                result = fn(*args, **kwargs)
                return result
            except ConnectFailure:
                if retries > 0:
                    info_msg = f'Failed to connect to OpenStack. Remaining retries {retries}'
                    logger.info(info_msg)
                else:
                    error_msg = f'Exception during OpenStack call to method {fn}'
                    logger.error(error_msg)
                    raise

    def create(self, **tpl_args):
        """Wrap stack create."""
        fn = self._stacks.create
        self._robust_heat_call(fn, **tpl_args)

    def delete(self, resource_name):
        """Wrap stack delete."""
        fn = self._stacks.delete
        self._robust_heat_call(fn, resource_name)
