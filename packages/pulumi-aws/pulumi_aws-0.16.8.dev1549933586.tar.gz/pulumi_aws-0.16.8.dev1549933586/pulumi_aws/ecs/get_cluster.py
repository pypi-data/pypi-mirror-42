# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetClusterResult(object):
    """
    A collection of values returned by getCluster.
    """
    def __init__(__self__, arn=None, pending_tasks_count=None, registered_container_instances_count=None, running_tasks_count=None, status=None, id=None):
        if arn and not isinstance(arn, str):
            raise TypeError('Expected argument arn to be a str')
        __self__.arn = arn
        """
        The ARN of the ECS Cluster
        """
        if pending_tasks_count and not isinstance(pending_tasks_count, int):
            raise TypeError('Expected argument pending_tasks_count to be a int')
        __self__.pending_tasks_count = pending_tasks_count
        """
        The number of pending tasks for the ECS Cluster
        """
        if registered_container_instances_count and not isinstance(registered_container_instances_count, int):
            raise TypeError('Expected argument registered_container_instances_count to be a int')
        __self__.registered_container_instances_count = registered_container_instances_count
        """
        The number of registered container instances for the ECS Cluster
        """
        if running_tasks_count and not isinstance(running_tasks_count, int):
            raise TypeError('Expected argument running_tasks_count to be a int')
        __self__.running_tasks_count = running_tasks_count
        """
        The number of running tasks for the ECS Cluster
        """
        if status and not isinstance(status, str):
            raise TypeError('Expected argument status to be a str')
        __self__.status = status
        """
        The status of the ECS Cluster
        """
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_cluster(cluster_name=None):
    """
    The ECS Cluster data source allows access to details of a specific
    cluster within an AWS ECS service.
    """
    __args__ = dict()

    __args__['clusterName'] = cluster_name
    __ret__ = await pulumi.runtime.invoke('aws:ecs/getCluster:getCluster', __args__)

    return GetClusterResult(
        arn=__ret__.get('arn'),
        pending_tasks_count=__ret__.get('pendingTasksCount'),
        registered_container_instances_count=__ret__.get('registeredContainerInstancesCount'),
        running_tasks_count=__ret__.get('runningTasksCount'),
        status=__ret__.get('status'),
        id=__ret__.get('id'))
