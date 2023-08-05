# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class DomainIdentityVerification(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The ARN of the domain identity.
    """
    domain: pulumi.Output[str]
    """
    The domain name of the SES domain identity to verify.
    """
    def __init__(__self__, resource_name, opts=None, domain=None, __name__=None, __opts__=None):
        """
        Represents a successful verification of an SES domain identity.
        
        Most commonly, this resource is used together with `aws_route53_record` and
        `aws_ses_domain_identity` to request an SES domain identity,
        deploy the required DNS verification records, and wait for verification to complete.
        
        > **WARNING:** This resource implements a part of the verification workflow. It does not represent a real-world entity in AWS, therefore changing or deleting this resource on its own has no immediate effect.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain: The domain name of the SES domain identity to verify.
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

        if domain is None:
            raise TypeError('Missing required property domain')
        __props__['domain'] = domain

        __props__['arn'] = None

        super(DomainIdentityVerification, __self__).__init__(
            'aws:ses/domainIdentityVerification:DomainIdentityVerification',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

