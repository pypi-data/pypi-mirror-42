# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetLogProfileResult(object):
    """
    A collection of values returned by getLogProfile.
    """
    def __init__(__self__, categories=None, locations=None, retention_policy=None, servicebus_rule_id=None, storage_account_id=None, id=None):
        if categories and not isinstance(categories, list):
            raise TypeError('Expected argument categories to be a list')
        __self__.categories = categories
        """
        List of categories of the logs.
        """
        if locations and not isinstance(locations, list):
            raise TypeError('Expected argument locations to be a list')
        __self__.locations = locations
        """
        List of regions for which Activity Log events are stored or streamed.
        """
        if retention_policy and not isinstance(retention_policy, dict):
            raise TypeError('Expected argument retention_policy to be a dict')
        __self__.retention_policy = retention_policy
        if servicebus_rule_id and not isinstance(servicebus_rule_id, str):
            raise TypeError('Expected argument servicebus_rule_id to be a str')
        __self__.servicebus_rule_id = servicebus_rule_id
        """
        The service bus (or event hub) rule ID of the service bus (or event hub) namespace in which the Activity Log is streamed to.
        """
        if storage_account_id and not isinstance(storage_account_id, str):
            raise TypeError('Expected argument storage_account_id to be a str')
        __self__.storage_account_id = storage_account_id
        """
        The resource id of the storage account in which the Activity Log is stored.
        """
        if id and not isinstance(id, str):
            raise TypeError('Expected argument id to be a str')
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_log_profile(name=None):
    """
    Use this data source to access the properties of a Log Profile.
    """
    __args__ = dict()

    __args__['name'] = name
    __ret__ = await pulumi.runtime.invoke('azure:monitoring/getLogProfile:getLogProfile', __args__)

    return GetLogProfileResult(
        categories=__ret__.get('categories'),
        locations=__ret__.get('locations'),
        retention_policy=__ret__.get('retentionPolicy'),
        servicebus_rule_id=__ret__.get('servicebusRuleId'),
        storage_account_id=__ret__.get('storageAccountId'),
        id=__ret__.get('id'))
