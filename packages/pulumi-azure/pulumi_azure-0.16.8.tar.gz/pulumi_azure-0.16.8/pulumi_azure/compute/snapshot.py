# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Snapshot(pulumi.CustomResource):
    create_option: pulumi.Output[str]
    """
    Indicates how the snapshot is to be created. Possible values are `Copy` or `Import`. Changing this forces a new resource to be created.
    """
    disk_size_gb: pulumi.Output[int]
    """
    The size of the Snapshotted Disk in GB.
    """
    encryption_settings: pulumi.Output[dict]
    location: pulumi.Output[str]
    """
    Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the Snapshot resource. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to create the Snapshot. Changing this forces a new resource to be created.
    """
    source_resource_id: pulumi.Output[str]
    """
    Specifies a reference to an existing snapshot, when `create_option` is `Copy`. Changing this forces a new resource to be created.
    """
    source_uri: pulumi.Output[str]
    """
    Specifies the URI to a Managed or Unmanaged Disk. Changing this forces a new resource to be created.
    """
    storage_account_id: pulumi.Output[str]
    """
    Specifies the ID of an storage account. Used with `source_uri` to allow authorization during import of unmanaged blobs from a different subscription. Changing this forces a new resource to be created.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    def __init__(__self__, resource_name, opts=None, create_option=None, disk_size_gb=None, encryption_settings=None, location=None, name=None, resource_group_name=None, source_resource_id=None, source_uri=None, storage_account_id=None, tags=None, __name__=None, __opts__=None):
        """
        Manages a Disk Snapshot.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] create_option: Indicates how the snapshot is to be created. Possible values are `Copy` or `Import`. Changing this forces a new resource to be created.
        :param pulumi.Input[int] disk_size_gb: The size of the Snapshotted Disk in GB.
        :param pulumi.Input[dict] encryption_settings
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Snapshot resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Snapshot. Changing this forces a new resource to be created.
        :param pulumi.Input[str] source_resource_id: Specifies a reference to an existing snapshot, when `create_option` is `Copy`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] source_uri: Specifies the URI to a Managed or Unmanaged Disk. Changing this forces a new resource to be created.
        :param pulumi.Input[str] storage_account_id: Specifies the ID of an storage account. Used with `source_uri` to allow authorization during import of unmanaged blobs from a different subscription. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
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

        if create_option is None:
            raise TypeError('Missing required property create_option')
        __props__['create_option'] = create_option

        __props__['disk_size_gb'] = disk_size_gb

        __props__['encryption_settings'] = encryption_settings

        if location is None:
            raise TypeError('Missing required property location')
        __props__['location'] = location

        __props__['name'] = name

        if resource_group_name is None:
            raise TypeError('Missing required property resource_group_name')
        __props__['resource_group_name'] = resource_group_name

        __props__['source_resource_id'] = source_resource_id

        __props__['source_uri'] = source_uri

        __props__['storage_account_id'] = storage_account_id

        __props__['tags'] = tags

        super(Snapshot, __self__).__init__(
            'azure:compute/snapshot:Snapshot',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

