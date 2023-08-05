# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Endpoint(pulumi.CustomResource):
    content_types_to_compresses: pulumi.Output[list]
    """
    An array of strings that indicates a content types on which compression will be applied. The value for the elements should be MIME types.
    """
    geo_filters: pulumi.Output[list]
    """
    A set of Geo Filters for this CDN Endpoint. Each `geo_filter` block supports fields documented below.
    """
    host_name: pulumi.Output[str]
    is_compression_enabled: pulumi.Output[bool]
    """
    Indicates whether compression is to be enabled. Defaults to false.
    """
    is_http_allowed: pulumi.Output[bool]
    """
    Defaults to `true`.
    """
    is_https_allowed: pulumi.Output[bool]
    """
    Defaults to `true`.
    """
    location: pulumi.Output[str]
    """
    Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the CDN Endpoint. Changing this forces a new resource to be created.
    """
    optimization_type: pulumi.Output[str]
    """
    What types of optimization should this CDN Endpoint optimize for? Possible values include `DynamicSiteAcceleration`, `GeneralMediaStreaming`, `GeneralWebDelivery`, `LargeFileDownload` and `VideoOnDemandMediaStreaming`.
    """
    origins: pulumi.Output[list]
    """
    The set of origins of the CDN endpoint. When multiple origins exist, the first origin will be used as primary and rest will be used as failover options. Each `origin` block supports fields documented below.
    """
    origin_host_header: pulumi.Output[str]
    """
    The host header CDN provider will send along with content requests to origins. Defaults to the host name of the origin.
    """
    origin_path: pulumi.Output[str]
    """
    The path used at for origin requests.
    """
    probe_path: pulumi.Output[str]
    """
    the path to a file hosted on the origin which helps accelerate delivery of the dynamic content and calculate the most optimal routes for the CDN. This is relative to the `origin_path`.
    """
    profile_name: pulumi.Output[str]
    """
    The CDN Profile to which to attach the CDN Endpoint.
    """
    querystring_caching_behaviour: pulumi.Output[str]
    """
    Sets query string caching behavior. Allowed values are `IgnoreQueryString`, `BypassCaching` and `UseQueryString`. Defaults to `IgnoreQueryString`.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to create the CDN Endpoint.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    def __init__(__self__, resource_name, opts=None, content_types_to_compresses=None, geo_filters=None, is_compression_enabled=None, is_http_allowed=None, is_https_allowed=None, location=None, name=None, optimization_type=None, origins=None, origin_host_header=None, origin_path=None, probe_path=None, profile_name=None, querystring_caching_behaviour=None, resource_group_name=None, tags=None, __name__=None, __opts__=None):
        """
        A CDN Endpoint is the entity within a CDN Profile containing configuration information regarding caching behaviors and origins. The CDN Endpoint is exposed using the URL format <endpointname>.azureedge.net.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] content_types_to_compresses: An array of strings that indicates a content types on which compression will be applied. The value for the elements should be MIME types.
        :param pulumi.Input[list] geo_filters: A set of Geo Filters for this CDN Endpoint. Each `geo_filter` block supports fields documented below.
        :param pulumi.Input[bool] is_compression_enabled: Indicates whether compression is to be enabled. Defaults to false.
        :param pulumi.Input[bool] is_http_allowed: Defaults to `true`.
        :param pulumi.Input[bool] is_https_allowed: Defaults to `true`.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the CDN Endpoint. Changing this forces a new resource to be created.
        :param pulumi.Input[str] optimization_type: What types of optimization should this CDN Endpoint optimize for? Possible values include `DynamicSiteAcceleration`, `GeneralMediaStreaming`, `GeneralWebDelivery`, `LargeFileDownload` and `VideoOnDemandMediaStreaming`.
        :param pulumi.Input[list] origins: The set of origins of the CDN endpoint. When multiple origins exist, the first origin will be used as primary and rest will be used as failover options. Each `origin` block supports fields documented below.
        :param pulumi.Input[str] origin_host_header: The host header CDN provider will send along with content requests to origins. Defaults to the host name of the origin.
        :param pulumi.Input[str] origin_path: The path used at for origin requests.
        :param pulumi.Input[str] probe_path: the path to a file hosted on the origin which helps accelerate delivery of the dynamic content and calculate the most optimal routes for the CDN. This is relative to the `origin_path`.
        :param pulumi.Input[str] profile_name: The CDN Profile to which to attach the CDN Endpoint.
        :param pulumi.Input[str] querystring_caching_behaviour: Sets query string caching behavior. Allowed values are `IgnoreQueryString`, `BypassCaching` and `UseQueryString`. Defaults to `IgnoreQueryString`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the CDN Endpoint.
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

        __props__['content_types_to_compresses'] = content_types_to_compresses

        __props__['geo_filters'] = geo_filters

        __props__['is_compression_enabled'] = is_compression_enabled

        __props__['is_http_allowed'] = is_http_allowed

        __props__['is_https_allowed'] = is_https_allowed

        if location is None:
            raise TypeError('Missing required property location')
        __props__['location'] = location

        __props__['name'] = name

        __props__['optimization_type'] = optimization_type

        if origins is None:
            raise TypeError('Missing required property origins')
        __props__['origins'] = origins

        __props__['origin_host_header'] = origin_host_header

        __props__['origin_path'] = origin_path

        __props__['probe_path'] = probe_path

        if profile_name is None:
            raise TypeError('Missing required property profile_name')
        __props__['profile_name'] = profile_name

        __props__['querystring_caching_behaviour'] = querystring_caching_behaviour

        if resource_group_name is None:
            raise TypeError('Missing required property resource_group_name')
        __props__['resource_group_name'] = resource_group_name

        __props__['tags'] = tags

        __props__['host_name'] = None

        super(Endpoint, __self__).__init__(
            'azure:cdn/endpoint:Endpoint',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

