# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Accelerator(pulumi.CustomResource):
    attributes: pulumi.Output[dict]
    """
    The attributes of the accelerator. Fields documented below.
    """
    enabled: pulumi.Output[bool]
    """
    Indicates whether the accelerator is enabled. The value is true or false. The default value is true.
    """
    ip_address_type: pulumi.Output[str]
    """
    The value for the address type must be `IPV4`.
    """
    ip_sets: pulumi.Output[list]
    """
    IP address set associated with the accelerator.
    """
    name: pulumi.Output[str]
    """
    The name of the accelerator.
    """
    def __init__(__self__, resource_name, opts=None, attributes=None, enabled=None, ip_address_type=None, name=None, __name__=None, __opts__=None):
        """
        Provides a Global Accelerator accelerator.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] attributes: The attributes of the accelerator. Fields documented below.
        :param pulumi.Input[bool] enabled: Indicates whether the accelerator is enabled. The value is true or false. The default value is true.
        :param pulumi.Input[str] ip_address_type: The value for the address type must be `IPV4`.
        :param pulumi.Input[str] name: The name of the accelerator.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if not resource_name:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(resource_name, str):
            raise TypeError('Expected resource name to be a string')
        if opts and not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        __props__['attributes'] = attributes

        __props__['enabled'] = enabled

        __props__['ip_address_type'] = ip_address_type

        __props__['name'] = name

        __props__['ip_sets'] = None

        super(Accelerator, __self__).__init__(
            'aws:globalaccelerator/accelerator:Accelerator',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

