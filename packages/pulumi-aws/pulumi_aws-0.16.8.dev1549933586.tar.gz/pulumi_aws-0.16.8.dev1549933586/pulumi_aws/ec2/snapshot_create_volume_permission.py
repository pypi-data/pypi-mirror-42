# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class SnapshotCreateVolumePermission(pulumi.CustomResource):
    account_id: pulumi.Output[str]
    """
    An AWS Account ID to add create volume permissions
    """
    snapshot_id: pulumi.Output[str]
    """
    A snapshot ID
    """
    def __init__(__self__, resource_name, opts=None, account_id=None, snapshot_id=None, __name__=None, __opts__=None):
        """
        Adds permission to create volumes off of a given EBS Snapshot.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: An AWS Account ID to add create volume permissions
        :param pulumi.Input[str] snapshot_id: A snapshot ID
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

        if account_id is None:
            raise TypeError('Missing required property account_id')
        __props__['account_id'] = account_id

        if snapshot_id is None:
            raise TypeError('Missing required property snapshot_id')
        __props__['snapshot_id'] = snapshot_id

        super(SnapshotCreateVolumePermission, __self__).__init__(
            'aws:ec2/snapshotCreateVolumePermission:SnapshotCreateVolumePermission',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

