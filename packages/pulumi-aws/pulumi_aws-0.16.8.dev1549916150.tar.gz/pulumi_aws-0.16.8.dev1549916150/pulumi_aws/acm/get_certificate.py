# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetCertificateResult(object):
    """
    A collection of values returned by getCertificate.
    """
    def __init__(__self__, arn=None, id=None):
        if arn and not isinstance(arn, str):
            raise TypeError('Expected argument arn to be a str')
        __self__.arn = arn
        """
        Set to the ARN of the found certificate, suitable for referencing in other resources that support ACM certificates.
        """
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_certificate(domain=None, most_recent=None, statuses=None, types=None):
    """
    Use this data source to get the ARN of a certificate in AWS Certificate
    Manager (ACM), you can reference
    it by domain without having to hard code the ARNs as input.
    """
    __args__ = dict()

    __args__['domain'] = domain
    __args__['mostRecent'] = most_recent
    __args__['statuses'] = statuses
    __args__['types'] = types
    __ret__ = await pulumi.runtime.invoke('aws:acm/getCertificate:getCertificate', __args__)

    return GetCertificateResult(
        arn=__ret__.get('arn'),
        id=__ret__.get('id'))
