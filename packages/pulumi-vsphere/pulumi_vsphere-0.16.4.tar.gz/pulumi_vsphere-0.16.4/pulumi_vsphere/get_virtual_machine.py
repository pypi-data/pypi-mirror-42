# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from . import utilities, tables

class GetVirtualMachineResult(object):
    """
    A collection of values returned by getVirtualMachine.
    """
    def __init__(__self__, alternate_guest_name=None, disks=None, firmware=None, guest_id=None, network_interface_types=None, scsi_bus_sharing=None, scsi_type=None, id=None):
        if alternate_guest_name and not isinstance(alternate_guest_name, str):
            raise TypeError('Expected argument alternate_guest_name to be a str')
        __self__.alternate_guest_name = alternate_guest_name
        """
        The alternate guest name of the virtual machine when
        guest_id is a non-specific operating system, like `otherGuest`.
        """
        if disks and not isinstance(disks, list):
            raise TypeError('Expected argument disks to be a list')
        __self__.disks = disks
        """
        Information about each of the disks on this virtual machine or
        template. These are sorted by bus and unit number so that they can be applied
        to a `vsphere_virtual_machine` resource in the order the resource expects
        while cloning. This is useful for discovering certain disk settings while
        performing a linked clone, as all settings that are output by this data
        source must be the same on the destination virtual machine as the source.
        Only the first number of controllers defined by `scsi_controller_scan_count`
        are scanned for disks. The sub-attributes are:
        """
        if firmware and not isinstance(firmware, str):
            raise TypeError('Expected argument firmware to be a str')
        __self__.firmware = firmware
        """
        The firmware type for this virtual machine. Can be `bios` or `efi`.
        """
        if guest_id and not isinstance(guest_id, str):
            raise TypeError('Expected argument guest_id to be a str')
        __self__.guest_id = guest_id
        """
        The guest ID of the virtual machine or template.
        """
        if network_interface_types and not isinstance(network_interface_types, list):
            raise TypeError('Expected argument network_interface_types to be a list')
        __self__.network_interface_types = network_interface_types
        """
        The network interface types for each network
        interface found on the virtual machine, in device bus order. Will be one of
        `e1000`, `e1000e`, `pcnet32`, `sriov`, `vmxnet2`, or `vmxnet3`.
        """
        if scsi_bus_sharing and not isinstance(scsi_bus_sharing, str):
            raise TypeError('Expected argument scsi_bus_sharing to be a str')
        __self__.scsi_bus_sharing = scsi_bus_sharing
        """
        Mode for sharing the SCSI bus. The modes are
        physicalSharing, virtualSharing, and noSharing. Only the first number of
        controllers defined by `scsi_controller_scan_count` are scanned.
        """
        if scsi_type and not isinstance(scsi_type, str):
            raise TypeError('Expected argument scsi_type to be a str')
        __self__.scsi_type = scsi_type
        """
        The common type of all SCSI controllers on this virtual machine.
        Will be one of `lsilogic` (LSI Logic Parallel), `lsilogic-sas` (LSI Logic
        SAS), `pvscsi` (VMware Paravirtual), `buslogic` (BusLogic), or `mixed` when
        there are multiple controller types. Only the first number of controllers
        defined by `scsi_controller_scan_count` are scanned.
        """
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_virtual_machine(datacenter_id=None, name=None, scsi_controller_scan_count=None):
    """
    The `vsphere_virtual_machine` data source can be used to find the UUID of an
    existing virtual machine or template. Its most relevant purpose is for finding
    the UUID of a template to be used as the source for cloning into a new
    [`vsphere_virtual_machine`][docs-virtual-machine-resource] resource. It also
    reads the guest ID so that can be supplied as well.
    
    [docs-virtual-machine-resource]: /docs/providers/vsphere/r/virtual_machine.html
    """
    __args__ = dict()

    __args__['datacenterId'] = datacenter_id
    __args__['name'] = name
    __args__['scsiControllerScanCount'] = scsi_controller_scan_count
    __ret__ = await pulumi.runtime.invoke('vsphere:index/getVirtualMachine:getVirtualMachine', __args__)

    return GetVirtualMachineResult(
        alternate_guest_name=__ret__.get('alternateGuestName'),
        disks=__ret__.get('disks'),
        firmware=__ret__.get('firmware'),
        guest_id=__ret__.get('guestId'),
        network_interface_types=__ret__.get('networkInterfaceTypes'),
        scsi_bus_sharing=__ret__.get('scsiBusSharing'),
        scsi_type=__ret__.get('scsiType'),
        id=__ret__.get('id'))
