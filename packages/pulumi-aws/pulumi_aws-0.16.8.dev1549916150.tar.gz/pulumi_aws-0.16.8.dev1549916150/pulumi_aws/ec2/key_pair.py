# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class KeyPair(pulumi.CustomResource):
    fingerprint: pulumi.Output[str]
    """
    The MD5 public key fingerprint as specified in section 4 of RFC 4716.
    """
    key_name: pulumi.Output[str]
    """
    The name for the key pair.
    """
    key_name_prefix: pulumi.Output[str]
    """
    Creates a unique name beginning with the specified prefix. Conflicts with `key_name`.
    """
    public_key: pulumi.Output[str]
    """
    The public key material.
    """
    def __init__(__self__, resource_name, opts=None, key_name=None, key_name_prefix=None, public_key=None, __name__=None, __opts__=None):
        """
        Provides an [EC2 key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) resource. A key pair is used to control login access to EC2 instances.
        
        Currently this resource requires an existing user-supplied key pair. This key pair's public key will be registered with AWS to allow logging-in to EC2 instances.
        
        When importing an existing key pair the public key material may be in any format supported by AWS. Supported formats (per the [AWS documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#how-to-generate-your-own-key-and-import-it-to-aws)) are:
        
        * OpenSSH public key format (the format in ~/.ssh/authorized_keys)
        * Base64 encoded DER format
        * SSH public key file format as specified in RFC4716
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key_name: The name for the key pair.
        :param pulumi.Input[str] key_name_prefix: Creates a unique name beginning with the specified prefix. Conflicts with `key_name`.
        :param pulumi.Input[str] public_key: The public key material.
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

        __props__['key_name'] = key_name

        __props__['key_name_prefix'] = key_name_prefix

        if public_key is None:
            raise TypeError('Missing required property public_key')
        __props__['public_key'] = public_key

        __props__['fingerprint'] = None

        super(KeyPair, __self__).__init__(
            'aws:ec2/keyPair:KeyPair',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

