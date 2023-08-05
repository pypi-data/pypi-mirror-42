import logging

from ${resource_module_name}.resource import ${resource_class_name}

logger = logging.getLogger(__name__)

def deploy(context):
    ${resource_object_name} =  ${resource_class_name}(context)
    ${resource_object_name}.deploy(context)
    return ${resource_object_name}.endpoint

def clean(context):
    pass
