# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from . import utilities, tables

class ResourcePool(pulumi.CustomResource):
    cpu_expandable: pulumi.Output[bool]
    """
    Determines if the reservation on a resource
    pool can grow beyond the specified value if the parent resource pool has
    unreserved resources. Default: `true`
    """
    cpu_limit: pulumi.Output[int]
    """
    The CPU utilization of a resource pool will not exceed
    this limit, even if there are available resources. Set to `-1` for unlimited.
    Default: `-1`
    """
    cpu_reservation: pulumi.Output[int]
    """
    Amount of CPU (MHz) that is guaranteed
    available to the resource pool. Default: `0`
    """
    cpu_share_level: pulumi.Output[str]
    """
    The CPU allocation level. The level is a
    simplified view of shares. Levels map to a pre-determined set of numeric
    values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
    `low`, `normal`, or `high` are specified values in `cpu_shares` will be
    ignored.  Default: `normal`
    """
    cpu_shares: pulumi.Output[int]
    """
    The number of shares allocated for CPU. Used to
    determine resource allocation in case of resource contention. If this is set,
    `cpu_share_level` must be `custom`.
    """
    custom_attributes: pulumi.Output[dict]
    memory_expandable: pulumi.Output[bool]
    """
    Determines if the reservation on a resource
    pool can grow beyond the specified value if the parent resource pool has
    unreserved resources. Default: `true`
    """
    memory_limit: pulumi.Output[int]
    """
    The CPU utilization of a resource pool will not exceed
    this limit, even if there are available resources. Set to `-1` for unlimited.
    Default: `-1`
    """
    memory_reservation: pulumi.Output[int]
    """
    Amount of CPU (MHz) that is guaranteed
    available to the resource pool. Default: `0`
    """
    memory_share_level: pulumi.Output[str]
    """
    The CPU allocation level. The level is a
    simplified view of shares. Levels map to a pre-determined set of numeric
    values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
    `low`, `normal`, or `high` are specified values in `memory_shares` will be
    ignored.  Default: `normal`
    """
    memory_shares: pulumi.Output[int]
    """
    The number of shares allocated for CPU. Used to
    determine resource allocation in case of resource contention. If this is set,
    `memory_share_level` must be `custom`.
    """
    name: pulumi.Output[str]
    """
    The name of the resource pool.
    """
    parent_resource_pool_id: pulumi.Output[str]
    """
    The [managed object ID][docs-about-morefs]
    of the parent resource pool. This can be the root resource pool for a cluster
    or standalone host, or a resource pool itself. When moving a resource pool
    from one parent resource pool to another, both must share a common root
    resource pool or the move will fail.
    """
    tags: pulumi.Output[list]
    """
    The IDs of any tags to attach to this resource. See
    [here][docs-applying-tags] for a reference on how to apply tags.
    """
    def __init__(__self__, resource_name, opts=None, cpu_expandable=None, cpu_limit=None, cpu_reservation=None, cpu_share_level=None, cpu_shares=None, custom_attributes=None, memory_expandable=None, memory_limit=None, memory_reservation=None, memory_share_level=None, memory_shares=None, name=None, parent_resource_pool_id=None, tags=None, __name__=None, __opts__=None):
        """
        The `vsphere_resource_pool` resource can be used to create and manage
        resource pools in standalone hosts or on compute clusters.
        
        For more information on vSphere resource pools, see [this
        page][ref-vsphere-resource_pools].
        
        [ref-vsphere-resource_pools]: https://docs.vmware.com/en/VMware-vSphere/6.5/com.vmware.vsphere.resmgmt.doc/GUID-60077B40-66FF-4625-934A-641703ED7601.html
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] cpu_expandable: Determines if the reservation on a resource
               pool can grow beyond the specified value if the parent resource pool has
               unreserved resources. Default: `true`
        :param pulumi.Input[int] cpu_limit: The CPU utilization of a resource pool will not exceed
               this limit, even if there are available resources. Set to `-1` for unlimited.
               Default: `-1`
        :param pulumi.Input[int] cpu_reservation: Amount of CPU (MHz) that is guaranteed
               available to the resource pool. Default: `0`
        :param pulumi.Input[str] cpu_share_level: The CPU allocation level. The level is a
               simplified view of shares. Levels map to a pre-determined set of numeric
               values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
               `low`, `normal`, or `high` are specified values in `cpu_shares` will be
               ignored.  Default: `normal`
        :param pulumi.Input[int] cpu_shares: The number of shares allocated for CPU. Used to
               determine resource allocation in case of resource contention. If this is set,
               `cpu_share_level` must be `custom`.
        :param pulumi.Input[dict] custom_attributes
        :param pulumi.Input[bool] memory_expandable: Determines if the reservation on a resource
               pool can grow beyond the specified value if the parent resource pool has
               unreserved resources. Default: `true`
        :param pulumi.Input[int] memory_limit: The CPU utilization of a resource pool will not exceed
               this limit, even if there are available resources. Set to `-1` for unlimited.
               Default: `-1`
        :param pulumi.Input[int] memory_reservation: Amount of CPU (MHz) that is guaranteed
               available to the resource pool. Default: `0`
        :param pulumi.Input[str] memory_share_level: The CPU allocation level. The level is a
               simplified view of shares. Levels map to a pre-determined set of numeric
               values for shares. Can be one of `low`, `normal`, `high`, or `custom`. When
               `low`, `normal`, or `high` are specified values in `memory_shares` will be
               ignored.  Default: `normal`
        :param pulumi.Input[int] memory_shares: The number of shares allocated for CPU. Used to
               determine resource allocation in case of resource contention. If this is set,
               `memory_share_level` must be `custom`.
        :param pulumi.Input[str] name: The name of the resource pool.
        :param pulumi.Input[str] parent_resource_pool_id: The [managed object ID][docs-about-morefs]
               of the parent resource pool. This can be the root resource pool for a cluster
               or standalone host, or a resource pool itself. When moving a resource pool
               from one parent resource pool to another, both must share a common root
               resource pool or the move will fail.
        :param pulumi.Input[list] tags: The IDs of any tags to attach to this resource. See
               [here][docs-applying-tags] for a reference on how to apply tags.
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

        __props__['cpu_expandable'] = cpu_expandable

        __props__['cpu_limit'] = cpu_limit

        __props__['cpu_reservation'] = cpu_reservation

        __props__['cpu_share_level'] = cpu_share_level

        __props__['cpu_shares'] = cpu_shares

        __props__['custom_attributes'] = custom_attributes

        __props__['memory_expandable'] = memory_expandable

        __props__['memory_limit'] = memory_limit

        __props__['memory_reservation'] = memory_reservation

        __props__['memory_share_level'] = memory_share_level

        __props__['memory_shares'] = memory_shares

        __props__['name'] = name

        if parent_resource_pool_id is None:
            raise TypeError('Missing required property parent_resource_pool_id')
        __props__['parent_resource_pool_id'] = parent_resource_pool_id

        __props__['tags'] = tags

        super(ResourcePool, __self__).__init__(
            'vsphere:index/resourcePool:ResourcePool',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

