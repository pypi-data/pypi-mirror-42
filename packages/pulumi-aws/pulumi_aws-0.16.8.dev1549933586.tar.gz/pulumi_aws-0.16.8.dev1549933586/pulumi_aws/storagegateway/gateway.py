# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Gateway(pulumi.CustomResource):
    activation_key: pulumi.Output[str]
    """
    Gateway activation key during resource creation. Conflicts with `gateway_ip_address`. Additional information is available in the [Storage Gateway User Guide](https://docs.aws.amazon.com/storagegateway/latest/userguide/get-activation-key.html).
    """
    arn: pulumi.Output[str]
    """
    Amazon Resource Name (ARN) of the gateway.
    """
    gateway_id: pulumi.Output[str]
    """
    Identifier of the gateway.
    """
    gateway_ip_address: pulumi.Output[str]
    """
    Gateway IP address to retrieve activation key during resource creation. Conflicts with `activation_key`. Gateway must be accessible on port 80 from where Terraform is running. Additional information is available in the [Storage Gateway User Guide](https://docs.aws.amazon.com/storagegateway/latest/userguide/get-activation-key.html).
    """
    gateway_name: pulumi.Output[str]
    """
    Name of the gateway.
    """
    gateway_timezone: pulumi.Output[str]
    """
    Time zone for the gateway. The time zone is of the format "GMT", "GMT-hr:mm", or "GMT+hr:mm". For example, `GMT-4:00` indicates the time is 4 hours behind GMT. The time zone is used, for example, for scheduling snapshots and your gateway's maintenance schedule.
    """
    gateway_type: pulumi.Output[str]
    """
    Type of the gateway. The default value is `STORED`. Valid values: `CACHED`, `FILE_S3`, `STORED`, `VTL`.
    """
    medium_changer_type: pulumi.Output[str]
    smb_active_directory_settings: pulumi.Output[dict]
    """
    Nested argument with Active Directory domain join information for Server Message Block (SMB) file shares. Only valid for `FILE_S3` gateway type. Must be set before creating `ActiveDirectory` authentication SMB file shares. More details below.
    """
    smb_guest_password: pulumi.Output[str]
    """
    Guest password for Server Message Block (SMB) file shares. Only valid for `FILE_S3` gateway type. Must be set before creating `GuestAccess` authentication SMB file shares. Terraform can only detect drift of the existence of a guest password, not its actual value from the gateway. Terraform can however update the password with changing the argument.
    """
    tape_drive_type: pulumi.Output[str]
    """
    Type of tape drive to use for tape gateway. Terraform cannot detect drift of this argument. Valid values: `IBM-ULT3580-TD5`.
    """
    def __init__(__self__, resource_name, opts=None, activation_key=None, gateway_ip_address=None, gateway_name=None, gateway_timezone=None, gateway_type=None, medium_changer_type=None, smb_active_directory_settings=None, smb_guest_password=None, tape_drive_type=None, __name__=None, __opts__=None):
        """
        Manages an AWS Storage Gateway file, tape, or volume gateway in the provider region.
        
        > NOTE: The Storage Gateway API requires the gateway to be connected to properly return information after activation. If you are receiving `The specified gateway is not connected` errors during resource creation (gateway activation), ensure your gateway instance meets the [Storage Gateway requirements](https://docs.aws.amazon.com/storagegateway/latest/userguide/Requirements.html).
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] activation_key: Gateway activation key during resource creation. Conflicts with `gateway_ip_address`. Additional information is available in the [Storage Gateway User Guide](https://docs.aws.amazon.com/storagegateway/latest/userguide/get-activation-key.html).
        :param pulumi.Input[str] gateway_ip_address: Gateway IP address to retrieve activation key during resource creation. Conflicts with `activation_key`. Gateway must be accessible on port 80 from where Terraform is running. Additional information is available in the [Storage Gateway User Guide](https://docs.aws.amazon.com/storagegateway/latest/userguide/get-activation-key.html).
        :param pulumi.Input[str] gateway_name: Name of the gateway.
        :param pulumi.Input[str] gateway_timezone: Time zone for the gateway. The time zone is of the format "GMT", "GMT-hr:mm", or "GMT+hr:mm". For example, `GMT-4:00` indicates the time is 4 hours behind GMT. The time zone is used, for example, for scheduling snapshots and your gateway's maintenance schedule.
        :param pulumi.Input[str] gateway_type: Type of the gateway. The default value is `STORED`. Valid values: `CACHED`, `FILE_S3`, `STORED`, `VTL`.
        :param pulumi.Input[str] medium_changer_type
        :param pulumi.Input[dict] smb_active_directory_settings: Nested argument with Active Directory domain join information for Server Message Block (SMB) file shares. Only valid for `FILE_S3` gateway type. Must be set before creating `ActiveDirectory` authentication SMB file shares. More details below.
        :param pulumi.Input[str] smb_guest_password: Guest password for Server Message Block (SMB) file shares. Only valid for `FILE_S3` gateway type. Must be set before creating `GuestAccess` authentication SMB file shares. Terraform can only detect drift of the existence of a guest password, not its actual value from the gateway. Terraform can however update the password with changing the argument.
        :param pulumi.Input[str] tape_drive_type: Type of tape drive to use for tape gateway. Terraform cannot detect drift of this argument. Valid values: `IBM-ULT3580-TD5`.
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

        __props__['activation_key'] = activation_key

        __props__['gateway_ip_address'] = gateway_ip_address

        if gateway_name is None:
            raise TypeError('Missing required property gateway_name')
        __props__['gateway_name'] = gateway_name

        if gateway_timezone is None:
            raise TypeError('Missing required property gateway_timezone')
        __props__['gateway_timezone'] = gateway_timezone

        __props__['gateway_type'] = gateway_type

        __props__['medium_changer_type'] = medium_changer_type

        __props__['smb_active_directory_settings'] = smb_active_directory_settings

        __props__['smb_guest_password'] = smb_guest_password

        __props__['tape_drive_type'] = tape_drive_type

        __props__['arn'] = None
        __props__['gateway_id'] = None

        super(Gateway, __self__).__init__(
            'aws:storagegateway/gateway:Gateway',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

