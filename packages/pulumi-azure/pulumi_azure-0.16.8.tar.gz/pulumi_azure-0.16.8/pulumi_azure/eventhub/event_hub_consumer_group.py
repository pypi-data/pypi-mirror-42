# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class EventHubConsumerGroup(pulumi.CustomResource):
    eventhub_name: pulumi.Output[str]
    """
    Specifies the name of the EventHub. Changing this forces a new resource to be created.
    """
    location: pulumi.Output[str]
    name: pulumi.Output[str]
    """
    Specifies the name of the EventHub Consumer Group resource. Changing this forces a new resource to be created.
    """
    namespace_name: pulumi.Output[str]
    """
    Specifies the name of the grandparent EventHub Namespace. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which the EventHub Consumer Group's grandparent Namespace exists. Changing this forces a new resource to be created.
    """
    user_metadata: pulumi.Output[str]
    """
    Specifies the user metadata.
    """
    def __init__(__self__, resource_name, opts=None, eventhub_name=None, location=None, name=None, namespace_name=None, resource_group_name=None, user_metadata=None, __name__=None, __opts__=None):
        """
        Manages a Event Hubs Consumer Group as a nested resource within an Event Hub.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] eventhub_name: Specifies the name of the EventHub. Changing this forces a new resource to be created.
        :param pulumi.Input[str] location
        :param pulumi.Input[str] name: Specifies the name of the EventHub Consumer Group resource. Changing this forces a new resource to be created.
        :param pulumi.Input[str] namespace_name: Specifies the name of the grandparent EventHub Namespace. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which the EventHub Consumer Group's grandparent Namespace exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] user_metadata: Specifies the user metadata.
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

        if eventhub_name is None:
            raise TypeError('Missing required property eventhub_name')
        __props__['eventhub_name'] = eventhub_name

        __props__['location'] = location

        __props__['name'] = name

        if namespace_name is None:
            raise TypeError('Missing required property namespace_name')
        __props__['namespace_name'] = namespace_name

        if resource_group_name is None:
            raise TypeError('Missing required property resource_group_name')
        __props__['resource_group_name'] = resource_group_name

        __props__['user_metadata'] = user_metadata

        super(EventHubConsumerGroup, __self__).__init__(
            'azure:eventhub/eventHubConsumerGroup:EventHubConsumerGroup',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

