# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetSecurityGroupResult(object):
    """
    A collection of values returned by getSecurityGroup.
    """
    def __init__(__self__, arn=None, description=None, id=None, name=None, tags=None, vpc_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError('Expected argument arn to be a str')
        __self__.arn = arn
        """
        The computed ARN of the security group.
        """
        if description and not isinstance(description, str):
            raise TypeError('Expected argument description to be a str')
        __self__.description = description
        """
        The description of the security group.
        """
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        if name and not isinstance(name, str):
            raise TypeError('Expected argument name to be a str')
        __self__.name = name
        if tags and not isinstance(tags, dict):
            raise TypeError('Expected argument tags to be a dict')
        __self__.tags = tags
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError('Expected argument vpc_id to be a str')
        __self__.vpc_id = vpc_id

async def get_security_group(filters=None, id=None, name=None, tags=None, vpc_id=None):
    """
    `aws_security_group` provides details about a specific Security Group.
    
    This resource can prove useful when a module accepts a Security Group id as
    an input variable and needs to, for example, determine the id of the
    VPC that the security group belongs to.
    """
    __args__ = dict()

    __args__['filters'] = filters
    __args__['id'] = id
    __args__['name'] = name
    __args__['tags'] = tags
    __args__['vpcId'] = vpc_id
    __ret__ = await pulumi.runtime.invoke('aws:ec2/getSecurityGroup:getSecurityGroup', __args__)

    return GetSecurityGroupResult(
        arn=__ret__.get('arn'),
        description=__ret__.get('description'),
        id=__ret__.get('id'),
        name=__ret__.get('name'),
        tags=__ret__.get('tags'),
        vpc_id=__ret__.get('vpcId'))
