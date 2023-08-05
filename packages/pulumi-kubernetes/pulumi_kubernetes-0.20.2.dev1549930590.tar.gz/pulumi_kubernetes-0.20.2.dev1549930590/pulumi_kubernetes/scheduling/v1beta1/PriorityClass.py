import pulumi
import pulumi.runtime

from ... import tables

class PriorityClass(pulumi.CustomResource):
    """
    PriorityClass defines mapping from a priority class name to the priority integer value. The
    value can be any valid integer.
    """
    def __init__(self, __name__, __opts__=None, description=None, global_default=None, metadata=None, value=None):
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        __props__['apiVersion'] = 'scheduling.k8s.io/v1beta1'
        __props__['kind'] = 'PriorityClass'
        if value is None:
            raise TypeError('Missing required property value')
        __props__['value'] = value
        __props__['description'] = description
        __props__['globalDefault'] = global_default
        __props__['metadata'] = metadata

        super(PriorityClass, self).__init__(
            "kubernetes:scheduling.k8s.io/v1beta1:PriorityClass",
            __name__,
            __props__,
            __opts__)

    def translate_output_property(self, prop: str) -> str:
        return tables._CASING_FORWARD_TABLE.get(prop) or prop

    def translate_input_property(self, prop: str) -> str:
        return tables._CASING_BACKWARD_TABLE.get(prop) or prop
