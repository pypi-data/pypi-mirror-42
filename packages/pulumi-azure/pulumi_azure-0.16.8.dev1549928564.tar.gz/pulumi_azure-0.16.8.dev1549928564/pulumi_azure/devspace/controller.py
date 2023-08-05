# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Controller(pulumi.CustomResource):
    data_plane_fqdn: pulumi.Output[str]
    """
    DNS name for accessing DataPlane services.
    """
    host_suffix: pulumi.Output[str]
    """
    The host suffix for the DevSpace Controller. Changing this forces a new resource to be created.
    """
    location: pulumi.Output[str]
    """
    Specifies the supported location where the DevSpace Controller should exist. Changing this forces a new resource to be created.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the DevSpace Controller. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group under which the DevSpace Controller resource has to be created. Changing this forces a new resource to be created.
    """
    sku: pulumi.Output[dict]
    """
    A `sku` block as documented below. Changing this forces a new resource to be created.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    target_container_host_credentials_base64: pulumi.Output[str]
    """
    Base64 encoding of `kube_config_raw` of Azure Kubernetes Service cluster. Changing this forces a new resource to be created.
    """
    target_container_host_resource_id: pulumi.Output[str]
    """
    The resource id of Azure Kubernetes Service cluster. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, host_suffix=None, location=None, name=None, resource_group_name=None, sku=None, tags=None, target_container_host_credentials_base64=None, target_container_host_resource_id=None, __name__=None, __opts__=None):
        """
        Manages a DevSpace Controller.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] host_suffix: The host suffix for the DevSpace Controller. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location: Specifies the supported location where the DevSpace Controller should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the DevSpace Controller. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group under which the DevSpace Controller resource has to be created. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] sku: A `sku` block as documented below. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] target_container_host_credentials_base64: Base64 encoding of `kube_config_raw` of Azure Kubernetes Service cluster. Changing this forces a new resource to be created.
        :param pulumi.Input[str] target_container_host_resource_id: The resource id of Azure Kubernetes Service cluster. Changing this forces a new resource to be created.
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

        if host_suffix is None:
            raise TypeError('Missing required property host_suffix')
        __props__['host_suffix'] = host_suffix

        if location is None:
            raise TypeError('Missing required property location')
        __props__['location'] = location

        __props__['name'] = name

        if resource_group_name is None:
            raise TypeError('Missing required property resource_group_name')
        __props__['resource_group_name'] = resource_group_name

        if sku is None:
            raise TypeError('Missing required property sku')
        __props__['sku'] = sku

        __props__['tags'] = tags

        if target_container_host_credentials_base64 is None:
            raise TypeError('Missing required property target_container_host_credentials_base64')
        __props__['target_container_host_credentials_base64'] = target_container_host_credentials_base64

        if target_container_host_resource_id is None:
            raise TypeError('Missing required property target_container_host_resource_id')
        __props__['target_container_host_resource_id'] = target_container_host_resource_id

        __props__['data_plane_fqdn'] = None

        super(Controller, __self__).__init__(
            'azure:devspace/controller:Controller',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

