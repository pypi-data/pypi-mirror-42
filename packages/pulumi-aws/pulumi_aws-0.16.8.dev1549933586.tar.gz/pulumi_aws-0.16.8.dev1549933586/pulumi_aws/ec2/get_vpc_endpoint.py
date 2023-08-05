# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetVpcEndpointResult(object):
    """
    A collection of values returned by getVpcEndpoint.
    """
    def __init__(__self__, cidr_blocks=None, dns_entries=None, id=None, network_interface_ids=None, policy=None, prefix_list_id=None, private_dns_enabled=None, route_table_ids=None, security_group_ids=None, service_name=None, state=None, subnet_ids=None, vpc_endpoint_type=None, vpc_id=None):
        if cidr_blocks and not isinstance(cidr_blocks, list):
            raise TypeError('Expected argument cidr_blocks to be a list')
        __self__.cidr_blocks = cidr_blocks
        """
        The list of CIDR blocks for the exposed AWS service. Applicable for endpoints of type `Gateway`.
        """
        if dns_entries and not isinstance(dns_entries, list):
            raise TypeError('Expected argument dns_entries to be a list')
        __self__.dns_entries = dns_entries
        """
        The DNS entries for the VPC Endpoint. Applicable for endpoints of type `Interface`. DNS blocks are documented below.
        """
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        if network_interface_ids and not isinstance(network_interface_ids, list):
            raise TypeError('Expected argument network_interface_ids to be a list')
        __self__.network_interface_ids = network_interface_ids
        """
        One or more network interfaces for the VPC Endpoint. Applicable for endpoints of type `Interface`.
        """
        if policy and not isinstance(policy, str):
            raise TypeError('Expected argument policy to be a str')
        __self__.policy = policy
        """
        The policy document associated with the VPC Endpoint. Applicable for endpoints of type `Gateway`.
        """
        if prefix_list_id and not isinstance(prefix_list_id, str):
            raise TypeError('Expected argument prefix_list_id to be a str')
        __self__.prefix_list_id = prefix_list_id
        """
        The prefix list ID of the exposed AWS service. Applicable for endpoints of type `Gateway`.
        """
        if private_dns_enabled and not isinstance(private_dns_enabled, bool):
            raise TypeError('Expected argument private_dns_enabled to be a bool')
        __self__.private_dns_enabled = private_dns_enabled
        """
        Whether or not the VPC is associated with a private hosted zone - `true` or `false`. Applicable for endpoints of type `Interface`.
        """
        if route_table_ids and not isinstance(route_table_ids, list):
            raise TypeError('Expected argument route_table_ids to be a list')
        __self__.route_table_ids = route_table_ids
        """
        One or more route tables associated with the VPC Endpoint. Applicable for endpoints of type `Gateway`.
        """
        if security_group_ids and not isinstance(security_group_ids, list):
            raise TypeError('Expected argument security_group_ids to be a list')
        __self__.security_group_ids = security_group_ids
        """
        One or more security groups associated with the network interfaces. Applicable for endpoints of type `Interface`.
        """
        if service_name and not isinstance(service_name, str):
            raise TypeError('Expected argument service_name to be a str')
        __self__.service_name = service_name
        if state and not isinstance(state, str):
            raise TypeError('Expected argument state to be a str')
        __self__.state = state
        if subnet_ids and not isinstance(subnet_ids, list):
            raise TypeError('Expected argument subnet_ids to be a list')
        __self__.subnet_ids = subnet_ids
        """
        One or more subnets in which the VPC Endpoint is located. Applicable for endpoints of type `Interface`.
        """
        if vpc_endpoint_type and not isinstance(vpc_endpoint_type, str):
            raise TypeError('Expected argument vpc_endpoint_type to be a str')
        __self__.vpc_endpoint_type = vpc_endpoint_type
        """
        The VPC Endpoint type, `Gateway` or `Interface`.
        """
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError('Expected argument vpc_id to be a str')
        __self__.vpc_id = vpc_id

async def get_vpc_endpoint(id=None, service_name=None, state=None, vpc_id=None):
    """
    The VPC Endpoint data source provides details about
    a specific VPC endpoint.
    """
    __args__ = dict()

    __args__['id'] = id
    __args__['serviceName'] = service_name
    __args__['state'] = state
    __args__['vpcId'] = vpc_id
    __ret__ = await pulumi.runtime.invoke('aws:ec2/getVpcEndpoint:getVpcEndpoint', __args__)

    return GetVpcEndpointResult(
        cidr_blocks=__ret__.get('cidrBlocks'),
        dns_entries=__ret__.get('dnsEntries'),
        id=__ret__.get('id'),
        network_interface_ids=__ret__.get('networkInterfaceIds'),
        policy=__ret__.get('policy'),
        prefix_list_id=__ret__.get('prefixListId'),
        private_dns_enabled=__ret__.get('privateDnsEnabled'),
        route_table_ids=__ret__.get('routeTableIds'),
        security_group_ids=__ret__.get('securityGroupIds'),
        service_name=__ret__.get('serviceName'),
        state=__ret__.get('state'),
        subnet_ids=__ret__.get('subnetIds'),
        vpc_endpoint_type=__ret__.get('vpcEndpointType'),
        vpc_id=__ret__.get('vpcId'))
