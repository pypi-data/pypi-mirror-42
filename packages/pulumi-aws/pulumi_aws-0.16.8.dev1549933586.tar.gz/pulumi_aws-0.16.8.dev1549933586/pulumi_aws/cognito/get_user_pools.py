# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetUserPoolsResult(object):
    """
    A collection of values returned by getUserPools.
    """
    def __init__(__self__, arns=None, ids=None, id=None):
        if arns and not isinstance(arns, list):
            raise TypeError('Expected argument arns to be a list')
        __self__.arns = arns
        if ids and not isinstance(ids, list):
            raise TypeError('Expected argument ids to be a list')
        __self__.ids = ids
        """
        The list of cognito user pool ids.
        """
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_user_pools(name=None):
    """
    Use this data source to get a list of cognito user pools.
    """
    __args__ = dict()

    __args__['name'] = name
    __ret__ = await pulumi.runtime.invoke('aws:cognito/getUserPools:getUserPools', __args__)

    return GetUserPoolsResult(
        arns=__ret__.get('arns'),
        ids=__ret__.get('ids'),
        id=__ret__.get('id'))
