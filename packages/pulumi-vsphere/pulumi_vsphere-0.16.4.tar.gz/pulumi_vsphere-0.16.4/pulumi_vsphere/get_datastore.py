# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from . import utilities, tables

class GetDatastoreResult(object):
    """
    A collection of values returned by getDatastore.
    """
    def __init__(__self__, id=None):
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_datastore(datacenter_id=None, name=None):
    """
    The `vsphere_datastore` data source can be used to discover the ID of a
    datastore in vSphere. This is useful to fetch the ID of a datastore that you
    want to use to create virtual machines in using the
    [`vsphere_virtual_machine`][docs-virtual-machine-resource] resource. 
    
    [docs-virtual-machine-resource]: /docs/providers/vsphere/r/virtual_machine.html
    """
    __args__ = dict()

    __args__['datacenterId'] = datacenter_id
    __args__['name'] = name
    __ret__ = await pulumi.runtime.invoke('vsphere:index/getDatastore:getDatastore', __args__)

    return GetDatastoreResult(
        id=__ret__.get('id'))
