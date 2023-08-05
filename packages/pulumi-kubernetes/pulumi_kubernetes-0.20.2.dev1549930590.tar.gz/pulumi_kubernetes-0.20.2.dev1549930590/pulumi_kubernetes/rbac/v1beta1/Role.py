import pulumi
import pulumi.runtime

from ... import tables

class Role(pulumi.CustomResource):
    """
    Role is a namespaced, logical grouping of PolicyRules that can be referenced as a unit by a
    RoleBinding.
    """
    def __init__(self, __name__, __opts__=None, metadata=None, rules=None):
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        __props__['apiVersion'] = 'rbac.authorization.k8s.io/v1beta1'
        __props__['kind'] = 'Role'
        if rules is None:
            raise TypeError('Missing required property rules')
        __props__['rules'] = rules
        __props__['metadata'] = metadata

        super(Role, self).__init__(
            "kubernetes:rbac.authorization.k8s.io/v1beta1:Role",
            __name__,
            __props__,
            __opts__)

    def translate_output_property(self, prop: str) -> str:
        return tables._CASING_FORWARD_TABLE.get(prop) or prop

    def translate_input_property(self, prop: str) -> str:
        return tables._CASING_BACKWARD_TABLE.get(prop) or prop
