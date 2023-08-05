# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetInternetGatewayResult(object):
    """
    A collection of values returned by getInternetGateway.
    """
    def __init__(__self__, attachments=None, internet_gateway_id=None, owner_id=None, tags=None, id=None):
        if attachments and not isinstance(attachments, list):
            raise TypeError('Expected argument attachments to be a list')
        __self__.attachments = attachments
        if internet_gateway_id and not isinstance(internet_gateway_id, str):
            raise TypeError('Expected argument internet_gateway_id to be a str')
        __self__.internet_gateway_id = internet_gateway_id
        if owner_id and not isinstance(owner_id, str):
            raise TypeError('Expected argument owner_id to be a str')
        __self__.owner_id = owner_id
        """
        The ID of the AWS account that owns the internet gateway.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError('Expected argument tags to be a dict')
        __self__.tags = tags
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_internet_gateway(filters=None, internet_gateway_id=None, tags=None):
    """
    `aws_internet_gateway` provides details about a specific Internet Gateway.
    """
    __args__ = dict()

    __args__['filters'] = filters
    __args__['internetGatewayId'] = internet_gateway_id
    __args__['tags'] = tags
    __ret__ = await pulumi.runtime.invoke('aws:ec2/getInternetGateway:getInternetGateway', __args__)

    return GetInternetGatewayResult(
        attachments=__ret__.get('attachments'),
        internet_gateway_id=__ret__.get('internetGatewayId'),
        owner_id=__ret__.get('ownerId'),
        tags=__ret__.get('tags'),
        id=__ret__.get('id'))
