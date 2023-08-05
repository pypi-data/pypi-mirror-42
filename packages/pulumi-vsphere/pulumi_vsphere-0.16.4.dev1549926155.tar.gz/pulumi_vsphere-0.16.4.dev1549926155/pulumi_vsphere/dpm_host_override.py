# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from . import utilities, tables

class DpmHostOverride(pulumi.CustomResource):
    compute_cluster_id: pulumi.Output[str]
    """
    The [managed object reference
    ID][docs-about-morefs] of the cluster to put the override in.  Forces a new
    resource if changed.
    """
    dpm_automation_level: pulumi.Output[str]
    """
    The automation level for host power
    operations on this host. Can be one of `manual` or `automated`. Default:
    `manual`.
    """
    dpm_enabled: pulumi.Output[bool]
    """
    Enable DPM support for this host. Default:
    `false`.
    """
    host_system_id: pulumi.Output[str]
    def __init__(__self__, resource_name, opts=None, compute_cluster_id=None, dpm_automation_level=None, dpm_enabled=None, host_system_id=None, __name__=None, __opts__=None):
        """
        The `vsphere_dpm_host_override` resource can be used to add a DPM override to a
        cluster for a particular host. This allows you to control the power management
        settings for individual hosts in the cluster while leaving any unspecified ones
        at the default power management settings.
        
        For more information on DPM within vSphere clusters, see [this
        page][ref-vsphere-cluster-dpm].
        
        [ref-vsphere-cluster-dpm]: https://docs.vmware.com/en/VMware-vSphere/6.5/com.vmware.vsphere.resmgmt.doc/GUID-5E5E349A-4644-4C9C-B434-1C0243EBDC80.html
        
        > **NOTE:** This resource requires vCenter and is not available on direct ESXi
        connections.
        
        > **NOTE:** vSphere DRS requires a vSphere Enterprise Plus license.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] compute_cluster_id: The [managed object reference
               ID][docs-about-morefs] of the cluster to put the override in.  Forces a new
               resource if changed.
        :param pulumi.Input[str] dpm_automation_level: The automation level for host power
               operations on this host. Can be one of `manual` or `automated`. Default:
               `manual`.
        :param pulumi.Input[bool] dpm_enabled: Enable DPM support for this host. Default:
               `false`.
        :param pulumi.Input[str] host_system_id
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

        if compute_cluster_id is None:
            raise TypeError('Missing required property compute_cluster_id')
        __props__['compute_cluster_id'] = compute_cluster_id

        __props__['dpm_automation_level'] = dpm_automation_level

        __props__['dpm_enabled'] = dpm_enabled

        if host_system_id is None:
            raise TypeError('Missing required property host_system_id')
        __props__['host_system_id'] = host_system_id

        super(DpmHostOverride, __self__).__init__(
            'vsphere:index/dpmHostOverride:DpmHostOverride',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

