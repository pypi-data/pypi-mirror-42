# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from . import utilities, tables

class Tag(pulumi.CustomResource):
    category_id: pulumi.Output[str]
    """
    The unique identifier of the parent category in
    which this tag will be created. Forces a new resource if changed.
    """
    description: pulumi.Output[str]
    """
    A description for the tag.
    """
    name: pulumi.Output[str]
    """
    The display name of the tag. The name must be unique
    within its category.
    """
    def __init__(__self__, resource_name, opts=None, category_id=None, description=None, name=None, __name__=None, __opts__=None):
        """
        The `vsphere_tag` resource can be used to create and manage tags, which allow
        you to attach metadata to objects in the vSphere inventory to make these
        objects more sortable and searchable.
        
        For more information about tags, click [here][ext-tags-general].
        
        [ext-tags-general]: https://docs.vmware.com/en/VMware-vSphere/6.5/com.vmware.vsphere.vcenterhost.doc/GUID-E8E854DD-AA97-4E0C-8419-CE84F93C4058.html
        
        > **NOTE:** Tagging support is unsupported on direct ESXi connections and
        requires vCenter 6.0 or higher.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] category_id: The unique identifier of the parent category in
               which this tag will be created. Forces a new resource if changed.
        :param pulumi.Input[str] description: A description for the tag.
        :param pulumi.Input[str] name: The display name of the tag. The name must be unique
               within its category.
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

        if category_id is None:
            raise TypeError('Missing required property category_id')
        __props__['category_id'] = category_id

        __props__['description'] = description

        __props__['name'] = name

        super(Tag, __self__).__init__(
            'vsphere:index/tag:Tag',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

