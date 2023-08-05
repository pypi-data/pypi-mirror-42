import logging

from scotty.utils import ResourceUtils

logger = logging.getLogger(__name__)


class ${resource_class_name}(object):
    def __init__(self, context):
        self.resource_utils = ResourceUtils(context)
        self.resource = context.v1.resource

    def deploy(self):
        openstack = self.resource_utils.openstack
        params = {
            'public_net_id': openstack.public_net_id,
            'private_net_id': openstack.private_net_id,
            'private_subnet_id': openstack.private_subnet_id,
        }
        stack = openstack.deploy(resource.name, params)
        stack_outputs = openstack.parse_outputs(stack)
        self.endpoint = stack_outputs['endpoint']

    def clean(self):
        self.resource_utils.openstack.destroy(resource.name)
