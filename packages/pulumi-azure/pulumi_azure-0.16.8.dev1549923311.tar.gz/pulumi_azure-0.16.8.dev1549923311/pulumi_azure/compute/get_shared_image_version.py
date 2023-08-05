# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetSharedImageVersionResult(object):
    """
    A collection of values returned by getSharedImageVersion.
    """
    def __init__(__self__, exclude_from_latest=None, location=None, managed_image_id=None, tags=None, target_regions=None, id=None):
        if exclude_from_latest and not isinstance(exclude_from_latest, bool):
            raise TypeError('Expected argument exclude_from_latest to be a bool')
        __self__.exclude_from_latest = exclude_from_latest
        """
        Is this Image Version excluded from the `latest` filter?
        """
        if location and not isinstance(location, str):
            raise TypeError('Expected argument location to be a str')
        __self__.location = location
        """
        The supported Azure location where the Shared Image Gallery exists.
        """
        if managed_image_id and not isinstance(managed_image_id, str):
            raise TypeError('Expected argument managed_image_id to be a str')
        __self__.managed_image_id = managed_image_id
        """
        The ID of the Managed Image which was the source of this Shared Image Version.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError('Expected argument tags to be a dict')
        __self__.tags = tags
        """
        A mapping of tags assigned to the Shared Image.
        """
        if target_regions and not isinstance(target_regions, list):
            raise TypeError('Expected argument target_regions to be a list')
        __self__.target_regions = target_regions
        """
        One or more `target_region` blocks as documented below.
        """
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_shared_image_version(gallery_name=None, image_name=None, name=None, resource_group_name=None):
    """
    Use this data source to access information about an existing Version of a Shared Image within a Shared Image Gallery.
    
    > **NOTE** Shared Image Galleries are currently in Public Preview. You can find more information, including [how to register for the Public Preview here](https://azure.microsoft.com/en-gb/blog/announcing-the-public-preview-of-shared-image-gallery/).
    """
    __args__ = dict()

    __args__['galleryName'] = gallery_name
    __args__['imageName'] = image_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __ret__ = await pulumi.runtime.invoke('azure:compute/getSharedImageVersion:getSharedImageVersion', __args__)

    return GetSharedImageVersionResult(
        exclude_from_latest=__ret__.get('excludeFromLatest'),
        location=__ret__.get('location'),
        managed_image_id=__ret__.get('managedImageId'),
        tags=__ret__.get('tags'),
        target_regions=__ret__.get('targetRegions'),
        id=__ret__.get('id'))
