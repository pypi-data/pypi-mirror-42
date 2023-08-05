# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Cluster(pulumi.CustomResource):
    additional_info: pulumi.Output[str]
    """
    A JSON string for selecting additional features such as adding proxy information. Note: Currently there is no API to retrieve the value of this argument after EMR cluster creation from provider, therefore Terraform cannot detect drift from the actual EMR cluster if its value is changed outside Terraform.
    """
    applications: pulumi.Output[list]
    """
    A list of applications for the cluster. Valid values are: `Flink`, `Hadoop`, `Hive`, `Mahout`, `Pig`, `Spark`, and `JupyterHub` (as of EMR 5.14.0). Case insensitive
    """
    autoscaling_role: pulumi.Output[str]
    """
    An IAM role for automatic scaling policies. The IAM role provides permissions that the automatic scaling feature requires to launch and terminate EC2 instances in an instance group.
    """
    bootstrap_actions: pulumi.Output[list]
    """
    List of bootstrap actions that will be run before Hadoop is started on the cluster nodes. Defined below
    """
    cluster_state: pulumi.Output[str]
    configurations: pulumi.Output[str]
    """
    List of configurations supplied for the EMR cluster you are creating
    """
    configurations_json: pulumi.Output[str]
    """
    A JSON string for supplying list of configurations for the EMR cluster.
    """
    core_instance_count: pulumi.Output[int]
    """
    Number of Amazon EC2 instances used to execute the job flow. EMR will use one node as the cluster's master node and use the remainder of the nodes (`core_instance_count`-1) as core nodes. Cannot be specified if `instance_groups` is set. Default `1`
    """
    core_instance_type: pulumi.Output[str]
    """
    The EC2 instance type of the slave nodes. Cannot be specified if `instance_groups` is set
    """
    custom_ami_id: pulumi.Output[str]
    """
    A custom Amazon Linux AMI for the cluster (instead of an EMR-owned AMI). Available in Amazon EMR version 5.7.0 and later.
    """
    ebs_root_volume_size: pulumi.Output[int]
    """
    Size in GiB of the EBS root device volume of the Linux AMI that is used for each EC2 instance. Available in Amazon EMR version 4.x and later.
    """
    ec2_attributes: pulumi.Output[dict]
    """
    Attributes for the EC2 instances running the job flow. Defined below
    """
    instance_groups: pulumi.Output[list]
    """
    A list of `instance_group` objects for each instance group in the cluster. Exactly one of `master_instance_type` and `instance_group` must be specified. If `instance_group` is set, then it must contain a configuration block for at least the `MASTER` instance group type (as well as any additional instance groups). Defined below
    """
    keep_job_flow_alive_when_no_steps: pulumi.Output[bool]
    """
    Switch on/off run cluster with no steps or when all steps are complete (default is on)
    """
    kerberos_attributes: pulumi.Output[dict]
    """
    Kerberos configuration for the cluster. Defined below
    """
    log_uri: pulumi.Output[str]
    """
    S3 bucket to write the log files of the job flow. If a value is not provided, logs are not created
    """
    master_instance_type: pulumi.Output[str]
    """
    The EC2 instance type of the master node. Exactly one of `master_instance_type` and `instance_group` must be specified.
    """
    master_public_dns: pulumi.Output[str]
    """
    The public DNS name of the master EC2 instance.
    """
    name: pulumi.Output[str]
    """
    The name of the job flow
    """
    release_label: pulumi.Output[str]
    """
    The release label for the Amazon EMR release
    """
    scale_down_behavior: pulumi.Output[str]
    """
    The way that individual Amazon EC2 instances terminate when an automatic scale-in activity occurs or an `instance group` is resized.
    """
    security_configuration: pulumi.Output[str]
    """
    The security configuration name to attach to the EMR cluster. Only valid for EMR clusters with `release_label` 4.8.0 or greater
    """
    service_role: pulumi.Output[str]
    """
    IAM role that will be assumed by the Amazon EMR service to access AWS resources
    """
    steps: pulumi.Output[list]
    """
    List of steps to run when creating the cluster. Defined below. It is highly recommended to utilize the [lifecycle configuration block](https://www.terraform.io/docs/configuration/resources.html) with `ignore_changes` if other steps are being managed outside of Terraform.
    """
    tags: pulumi.Output[dict]
    """
    list of tags to apply to the EMR Cluster
    """
    termination_protection: pulumi.Output[bool]
    """
    Switch on/off termination protection (default is off)
    """
    visible_to_all_users: pulumi.Output[bool]
    """
    Whether the job flow is visible to all IAM users of the AWS account associated with the job flow. Default `true`
    """
    def __init__(__self__, resource_name, opts=None, additional_info=None, applications=None, autoscaling_role=None, bootstrap_actions=None, configurations=None, configurations_json=None, core_instance_count=None, core_instance_type=None, custom_ami_id=None, ebs_root_volume_size=None, ec2_attributes=None, instance_groups=None, keep_job_flow_alive_when_no_steps=None, kerberos_attributes=None, log_uri=None, master_instance_type=None, name=None, release_label=None, scale_down_behavior=None, security_configuration=None, service_role=None, steps=None, tags=None, termination_protection=None, visible_to_all_users=None, __name__=None, __opts__=None):
        """
        Provides an Elastic MapReduce Cluster, a web service that makes it easy to
        process large amounts of data efficiently. See [Amazon Elastic MapReduce Documentation](https://aws.amazon.com/documentation/elastic-mapreduce/)
        for more information.
        
        ## ec2_attributes
        
        Attributes for the Amazon EC2 instances running the job flow
        
        * `key_name` - (Optional) Amazon EC2 key pair that can be used to ssh to the master node as the user called `hadoop`
        * `subnet_id` - (Optional) VPC subnet id where you want the job flow to launch. Cannot specify the `cc1.4xlarge` instance type for nodes of a job flow launched in a Amazon VPC
        * `additional_master_security_groups` - (Optional) String containing a comma separated list of additional Amazon EC2 security group IDs for the master node
        * `additional_slave_security_groups` - (Optional) String containing a comma separated list of additional Amazon EC2 security group IDs for the slave nodes as a comma separated string
        * `emr_managed_master_security_group` - (Optional) Identifier of the Amazon EC2 EMR-Managed security group for the master node
        * `emr_managed_slave_security_group` - (Optional) Identifier of the Amazon EC2 EMR-Managed security group for the slave nodes
        * `service_access_security_group` - (Optional) Identifier of the Amazon EC2 service-access security group - required when the cluster runs on a private subnet
        * `instance_profile` - (Required) Instance Profile for EC2 instances of the cluster assume this role
        
        > **NOTE on EMR-Managed security groups:** These security groups will have any
        missing inbound or outbound access rules added and maintained by AWS, to ensure
        proper communication between instances in a cluster. The EMR service will
        maintain these rules for groups provided in `emr_managed_master_security_group`
        and `emr_managed_slave_security_group`; attempts to remove the required rules
        may succeed, only for the EMR service to re-add them in a matter of minutes.
        This may cause Terraform to fail to destroy an environment that contains an EMR
        cluster, because the EMR service does not revoke rules added on deletion,
        leaving a cyclic dependency between the security groups that prevents their
        deletion. To avoid this, use the `revoke_rules_on_delete` optional attribute for
        any Security Group used in `emr_managed_master_security_group` and
        `emr_managed_slave_security_group`. See [Amazon EMR-Managed Security
        Groups](http://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-man-sec-groups.html)
        for more information about the EMR-managed security group rules.
        
        ## kerberos_attributes
        
        Attributes for Kerberos configuration
        
        * `ad_domain_join_password` - (Optional) The Active Directory password for `ad_domain_join_user`
        * `ad_domain_join_user` - (Optional) Required only when establishing a cross-realm trust with an Active Directory domain. A user with sufficient privileges to join resources to the domain.
        * `cross_realm_trust_principal_password` - (Optional) Required only when establishing a cross-realm trust with a KDC in a different realm. The cross-realm principal password, which must be identical across realms.
        * `kdc_admin_password` - (Required) The password used within the cluster for the kadmin service on the cluster-dedicated KDC, which maintains Kerberos principals, password policies, and keytabs for the cluster.
        * `realm` - (Required) The name of the Kerberos realm to which all nodes in a cluster belong. For example, `EC2.INTERNAL`
        
        ## instance_group
        
        Attributes for each task instance group in the cluster
        
        * `instance_role` - (Required) The role of the instance group in the cluster. Valid values are: `MASTER`, `CORE`, and `TASK`.
        * `instance_type` - (Required) The EC2 instance type for all instances in the instance group
        * `instance_count` - (Optional) Target number of instances for the instance group
        * `name` - (Optional) Friendly name given to the instance group
        * `bid_price` - (Optional) If set, the bid price for each EC2 instance in the instance group, expressed in USD. By setting this attribute, the instance group is being declared as a Spot Instance, and will implicitly create a Spot request. Leave this blank to use On-Demand Instances. `bid_price` can not be set for the `MASTER` instance group, since that group must always be On-Demand
        * `ebs_config` - (Optional) A list of attributes for the EBS volumes attached to each instance in the instance group. Each `ebs_config` defined will result in additional EBS volumes being attached to _each_ instance in the instance group. Defined below
        * `autoscaling_policy` - (Optional) The autoscaling policy document. This is a JSON formatted string. See [EMR Auto Scaling](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-automatic-scaling.html)
        
        ## ebs_config
        
        Attributes for the EBS volumes attached to each EC2 instance in the `instance_group`
        
        * `size` - (Required) The volume size, in gibibytes (GiB).
        * `type` - (Required) The volume type. Valid options are `gp2`, `io1`, `standard` and `st1`. See [EBS Volume Types](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html).
        * `iops` - (Optional) The number of I/O operations per second (IOPS) that the volume supports
        * `volumes_per_instance` - (Optional) The number of EBS volumes with this configuration to attach to each EC2 instance in the instance group (default is 1)
        
        ## bootstrap_action
        
        * `name` - (Required) Name of the bootstrap action
        * `path` - (Required) Location of the script to run during a bootstrap action. Can be either a location in Amazon S3 or on a local file system
        * `args` - (Optional) List of command line arguments to pass to the bootstrap action script
        
        ## step
        
        Attributes for step configuration
        
        * `action_on_failure` - (Required) The action to take if the step fails. Valid values: `TERMINATE_JOB_FLOW`, `TERMINATE_CLUSTER`, `CANCEL_AND_WAIT`, and `CONTINUE`
        * `hadoop_jar_step` - (Required) The JAR file used for the step. Defined below.
        * `name` - (Required) The name of the step.
        
        ### hadoop_jar_step
        
        Attributes for Hadoop job step configuration
        
        * `args` - (Optional) List of command line arguments passed to the JAR file's main function when executed.
        * `jar` - (Required) Path to a JAR file run during the step.
        * `main_class` - (Optional) Name of the main class in the specified Java file. If not specified, the JAR file should specify a Main-Class in its manifest file.
        * `properties` - (Optional) Key-Value map of Java properties that are set when the step runs. You can use these properties to pass key value pairs to your main function.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] additional_info: A JSON string for selecting additional features such as adding proxy information. Note: Currently there is no API to retrieve the value of this argument after EMR cluster creation from provider, therefore Terraform cannot detect drift from the actual EMR cluster if its value is changed outside Terraform.
        :param pulumi.Input[list] applications: A list of applications for the cluster. Valid values are: `Flink`, `Hadoop`, `Hive`, `Mahout`, `Pig`, `Spark`, and `JupyterHub` (as of EMR 5.14.0). Case insensitive
        :param pulumi.Input[str] autoscaling_role: An IAM role for automatic scaling policies. The IAM role provides permissions that the automatic scaling feature requires to launch and terminate EC2 instances in an instance group.
        :param pulumi.Input[list] bootstrap_actions: List of bootstrap actions that will be run before Hadoop is started on the cluster nodes. Defined below
        :param pulumi.Input[str] configurations: List of configurations supplied for the EMR cluster you are creating
        :param pulumi.Input[str] configurations_json: A JSON string for supplying list of configurations for the EMR cluster.
        :param pulumi.Input[int] core_instance_count: Number of Amazon EC2 instances used to execute the job flow. EMR will use one node as the cluster's master node and use the remainder of the nodes (`core_instance_count`-1) as core nodes. Cannot be specified if `instance_groups` is set. Default `1`
        :param pulumi.Input[str] core_instance_type: The EC2 instance type of the slave nodes. Cannot be specified if `instance_groups` is set
        :param pulumi.Input[str] custom_ami_id: A custom Amazon Linux AMI for the cluster (instead of an EMR-owned AMI). Available in Amazon EMR version 5.7.0 and later.
        :param pulumi.Input[int] ebs_root_volume_size: Size in GiB of the EBS root device volume of the Linux AMI that is used for each EC2 instance. Available in Amazon EMR version 4.x and later.
        :param pulumi.Input[dict] ec2_attributes: Attributes for the EC2 instances running the job flow. Defined below
        :param pulumi.Input[list] instance_groups: A list of `instance_group` objects for each instance group in the cluster. Exactly one of `master_instance_type` and `instance_group` must be specified. If `instance_group` is set, then it must contain a configuration block for at least the `MASTER` instance group type (as well as any additional instance groups). Defined below
        :param pulumi.Input[bool] keep_job_flow_alive_when_no_steps: Switch on/off run cluster with no steps or when all steps are complete (default is on)
        :param pulumi.Input[dict] kerberos_attributes: Kerberos configuration for the cluster. Defined below
        :param pulumi.Input[str] log_uri: S3 bucket to write the log files of the job flow. If a value is not provided, logs are not created
        :param pulumi.Input[str] master_instance_type: The EC2 instance type of the master node. Exactly one of `master_instance_type` and `instance_group` must be specified.
        :param pulumi.Input[str] name: The name of the job flow
        :param pulumi.Input[str] release_label: The release label for the Amazon EMR release
        :param pulumi.Input[str] scale_down_behavior: The way that individual Amazon EC2 instances terminate when an automatic scale-in activity occurs or an `instance group` is resized.
        :param pulumi.Input[str] security_configuration: The security configuration name to attach to the EMR cluster. Only valid for EMR clusters with `release_label` 4.8.0 or greater
        :param pulumi.Input[str] service_role: IAM role that will be assumed by the Amazon EMR service to access AWS resources
        :param pulumi.Input[list] steps: List of steps to run when creating the cluster. Defined below. It is highly recommended to utilize the [lifecycle configuration block](https://www.terraform.io/docs/configuration/resources.html) with `ignore_changes` if other steps are being managed outside of Terraform.
        :param pulumi.Input[dict] tags: list of tags to apply to the EMR Cluster
        :param pulumi.Input[bool] termination_protection: Switch on/off termination protection (default is off)
        :param pulumi.Input[bool] visible_to_all_users: Whether the job flow is visible to all IAM users of the AWS account associated with the job flow. Default `true`
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

        __props__['additional_info'] = additional_info

        __props__['applications'] = applications

        __props__['autoscaling_role'] = autoscaling_role

        __props__['bootstrap_actions'] = bootstrap_actions

        __props__['configurations'] = configurations

        __props__['configurations_json'] = configurations_json

        __props__['core_instance_count'] = core_instance_count

        __props__['core_instance_type'] = core_instance_type

        __props__['custom_ami_id'] = custom_ami_id

        __props__['ebs_root_volume_size'] = ebs_root_volume_size

        __props__['ec2_attributes'] = ec2_attributes

        __props__['instance_groups'] = instance_groups

        __props__['keep_job_flow_alive_when_no_steps'] = keep_job_flow_alive_when_no_steps

        __props__['kerberos_attributes'] = kerberos_attributes

        __props__['log_uri'] = log_uri

        __props__['master_instance_type'] = master_instance_type

        __props__['name'] = name

        if release_label is None:
            raise TypeError('Missing required property release_label')
        __props__['release_label'] = release_label

        __props__['scale_down_behavior'] = scale_down_behavior

        __props__['security_configuration'] = security_configuration

        if service_role is None:
            raise TypeError('Missing required property service_role')
        __props__['service_role'] = service_role

        __props__['steps'] = steps

        __props__['tags'] = tags

        __props__['termination_protection'] = termination_protection

        __props__['visible_to_all_users'] = visible_to_all_users

        __props__['cluster_state'] = None
        __props__['master_public_dns'] = None

        super(Cluster, __self__).__init__(
            'aws:emr/cluster:Cluster',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

